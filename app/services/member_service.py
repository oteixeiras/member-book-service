from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from typing import Optional, Tuple, List
from app.models.member import Member
from app.models.address import Address
from app.models.contact_channel import ContactChannel
from app.models.additional_info import AdditionalInfo
from app.models.company import Company
from app.models.market_segmentation import MarketSegmentation
from app.models.performance import Performance
from app.models.member_company import MemberCompany
from app.models.profile import Profile
from app.dto.member_dto import MemberCreateDTO, MemberUpdateDTO
from app.dto.upsert_data_dto import UpsertDataRequestDTO
from app.dto.market_segmentation_dto import MarketSegmentationCreateDTO, MarketSegmentationUpdateDTO
from app.seeds.profiles_seed import seed_profiles
from datetime import datetime


class MemberService:
    """Service responsável pela lógica de negócio relacionada aos membros."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _validate_foreign_key(self, model_class, field_name, value):
        """Valida se uma foreign key existe na tabela."""
        if value is None or value == 0:
            return False
        return self.db.query(model_class).filter(getattr(model_class, field_name) == value).first() is not None
    
    def _safe_commit(self):
        """Faz commit seguro com tratamento de erros."""
        try:
            self.db.commit()
            return True
        except IntegrityError as e:
            self.db.rollback()
            raise Exception(f"Erro de integridade: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erro ao salvar dados: {str(e)}")
    
    async def populate_initial_data(self) -> dict:
        """
        Popula dados iniciais do sistema.
        Atualmente popula a tabela profiles com dados padrão.
        """
        try:
            # Executar seed dos profiles
            seed_profiles(self.db)
            
            return {
                "profiles_updated": True,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        except Exception as e:
            raise Exception(f"Erro ao popular dados iniciais: {str(e)}")
    
    async def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """Busca um membro pelo ID."""
        return self.db.query(Member).filter(Member.id == member_id).first()
    
    async def create_member(self, member_data: MemberCreateDTO) -> Member:
        """Cria um novo membro."""
        try:
            # Verificar se já existe um membro com o mesmo documento
            existing_member = self.db.query(Member).filter(
                Member.document == member_data.document
            ).first()
            
            if existing_member:
                raise ValueError("Já existe um membro com este documento")
            
            # Criar novo membro
            member = Member(**member_data.dict())
            self.db.add(member)
            self.db.commit()
            self.db.refresh(member)
            
            return member
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erro ao criar membro: {str(e)}")
    
    async def update_member(self, member_id: int, member_data: MemberUpdateDTO) -> Optional[Member]:
        """Atualiza um membro existente."""
        try:
            member = await self.get_member_by_id(member_id)
            if not member:
                return None
            
            # Verificar se o documento está sendo alterado e se já existe outro membro com ele
            if member_data.document and member_data.document != member.document:
                existing_member = self.db.query(Member).filter(
                    and_(Member.document == member_data.document, Member.id != member_id)
                ).first()
                
                if existing_member:
                    raise ValueError("Já existe outro membro com este documento")
            
            # Atualizar campos
            update_data = member_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(member, field, value)
            
            member.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(member)
            
            return member
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erro ao atualizar membro: {str(e)}")
    
    async def delete_member(self, member_id: int) -> bool:
        """Remove um membro."""
        try:
            member = await self.get_member_by_id(member_id)
            if not member:
                return False
            
            self.db.delete(member)
            self.db.commit()
            
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erro ao remover membro: {str(e)}")
    
    async def list_members(self, skip: int = 0, limit: int = 100) -> Tuple[List[Member], int]:
        """Lista membros com paginação."""
        try:
            # Buscar membros com paginação
            members = self.db.query(Member).offset(skip).limit(limit).all()
            
            # Contar total de membros
            total = self.db.query(Member).count()
            
            return members, total
        except Exception as e:
            raise Exception(f"Erro ao listar membros: {str(e)}")
    
    async def get_members_by_status(self, status: str, skip: int = 0, limit: int = 100) -> Tuple[List[Member], int]:
        """Lista membros por status com paginação."""
        try:
            # Buscar membros por status com paginação
            members = self.db.query(Member).filter(
                Member.status == status
            ).offset(skip).limit(limit).all()
            
            # Contar total de membros com este status
            total = self.db.query(Member).filter(Member.status == status).count()
            
            return members, total
        except Exception as e:
            raise Exception(f"Erro ao listar membros por status: {str(e)}")
    
    async def get_members_by_profile(self, profile_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[Member], int]:
        """Lista membros por perfil com paginação."""
        try:
            # Buscar membros por perfil com paginação
            members = self.db.query(Member).filter(
                Member.profile_id == profile_id
            ).offset(skip).limit(limit).all()
            
            # Contar total de membros com este perfil
            total = self.db.query(Member).filter(Member.profile_id == profile_id).count()
            
            return members, total
        except Exception as e:
            raise Exception(f"Erro ao listar membros por perfil: {str(e)}")
    
    async def upsert_data(self, request_data: UpsertDataRequestDTO) -> dict:
        """
        Cria ou atualiza dados do sistema.
        Suporta upsert de todas as tabelas relacionadas.
        Campos únicos duplicados são ignorados.
        Objetos vazios são desconsiderados.
        """
        try:
            created_count = {}
            updated_count = {}
            errors = []
            processed_company_ids: List[int] = []
            
            # Filtrar apenas objetos não vazios
            filtered_data = request_data.get_non_empty_objects()
            
            # Executar seed dos profiles primeiro (sempre)
            seed_profiles(self.db)
            created_count["profiles"] = 4  # 4 profiles padrão
            
            # Market Segmentations: removido deste endpoint. Use endpoint dedicado.
            
            # Upsert Companies
            if filtered_data.get("companies"):
                created_count["companies"] = 0
                updated_count["companies"] = 0
                
                for company_data in filtered_data["companies"]:
                    try:
                        # Normalizar documento (ignorar placeholders como "string", "0" ou vazio)
                        normalized_doc = None
                        if getattr(company_data, 'document', None):
                            doc_str = str(company_data.document).strip()
                            if doc_str and doc_str.lower() not in {"string"} and doc_str not in {"0"}:
                                normalized_doc = doc_str

                        # Verificar se já existe por CNPJ válido, senão tentar por nome
                        existing = None
                        if normalized_doc:
                            existing = self.db.query(Company).filter(Company.document == normalized_doc).first()
                        elif getattr(company_data, 'name', None):
                            existing = self.db.query(Company).filter(Company.name == company_data.name).first()
                        
                        if existing:
                            # Atualizar se necessário
                            company_dict = company_data.dict(exclude_unset=True, exclude={'address'})
                            # Sobrescrever documento com o normalizado
                            if 'document' in company_dict:
                                company_dict['document'] = normalized_doc
                            
                            # Validar foreign keys antes de atualizar
                            if 'market_segmentation_id' in company_dict and company_dict['market_segmentation_id']:
                                if not self._validate_foreign_key(MarketSegmentation, 'id', company_dict['market_segmentation_id']):
                                    errors.append(f"Market segmentation ID {company_dict['market_segmentation_id']} não existe")
                                    continue
                            
                            for key, value in company_dict.items():
                                if value is not None and getattr(existing, key) != value:
                                    setattr(existing, key, value)
                                    updated_count["companies"] += 1

                            # Adicionar ID da empresa processada
                            if existing.id not in processed_company_ids:
                                processed_company_ids.append(existing.id)
                        else:
                            # Criar novo (já filtrado, então sempre tem dados)
                            company_dict = company_data.dict(exclude_unset=True, exclude={'address'})
                            # Sobrescrever documento com o normalizado
                            if 'document' in company_dict:
                                company_dict['document'] = normalized_doc
                            
                            # Validar foreign keys antes de criar
                            if 'market_segmentation_id' in company_dict and company_dict['market_segmentation_id']:
                                if not self._validate_foreign_key(MarketSegmentation, 'id', company_dict['market_segmentation_id']):
                                    errors.append(f"Market segmentation ID {company_dict['market_segmentation_id']} não existe")
                                    continue
                            
                            # Criar endereço se fornecido
                            address_id = None
                            if company_data.address:
                                address_dict = company_data.address.dict(exclude_unset=True)
                                if address_dict:
                                    address = Address(**address_dict)
                                    self.db.add(address)
                                    self.db.flush()
                                    address_id = address.id
                            
                            if address_id:
                                company_dict['address_id'] = address_id
                            company = Company(**company_dict)
                            self.db.add(company)
                            # Garantir ID disponível para vinculação
                            self.db.flush()
                            if company.id and company.id not in processed_company_ids:
                                processed_company_ids.append(company.id)
                            created_count["companies"] += 1
                    except Exception as e:
                        errors.append(f"Erro ao processar empresa {company_data.name}: {str(e)}")
            
            # Upsert Members
            if filtered_data.get("members"):
                created_count["members"] = 0
                updated_count["members"] = 0
                
                for member_data in filtered_data["members"]:
                    try:
                        # Verificar se já existe por CPF
                        existing = None
                        if member_data.document:
                            existing = self.db.query(Member).filter(
                                Member.document == member_data.document
                            ).first()
                        
                        if existing:
                            # Atualizar se necessário
                            member_dict = member_data.dict(exclude_unset=True, exclude={'address', 'contact_channels', 'additional_info'})
                            
                            # Validar foreign keys antes de atualizar
                            if 'profile_id' in member_dict and member_dict['profile_id']:
                                if not self._validate_foreign_key(Profile, 'id', member_dict['profile_id']):
                                    errors.append(f"Profile ID {member_dict['profile_id']} não existe")
                                    continue
                            
                            for key, value in member_dict.items():
                                if value is not None and getattr(existing, key) != value:
                                    setattr(existing, key, value)
                                    updated_count["members"] += 1

                            # Vincular membro às empresas processadas (evitar duplicatas)
                            if processed_company_ids:
                                for company_id in processed_company_ids:
                                    existing_relation = self.db.query(MemberCompany).filter(
                                        and_(
                                            MemberCompany.member_id == existing.id,
                                            MemberCompany.company_id == company_id
                                        )
                                    ).first()
                                    if not existing_relation:
                                        self.db.add(MemberCompany(
                                            member_id=existing.id,
                                            company_id=company_id,
                                            created_at=datetime.utcnow()
                                        ))
                        else:
                            # Criar novo (já filtrado, então sempre tem dados)
                            member_dict = member_data.dict(exclude_unset=True, exclude={'address', 'contact_channels', 'additional_info'})
                            
                            # Validar foreign keys antes de criar
                            if 'profile_id' in member_dict and member_dict['profile_id']:
                                if not self._validate_foreign_key(Profile, 'id', member_dict['profile_id']):
                                    errors.append(f"Profile ID {member_dict['profile_id']} não existe")
                                    continue
                            
                            # Criar endereço se fornecido
                            address_id = None
                            if member_data.address:
                                address_dict = member_data.address.dict(exclude_unset=True)
                                if address_dict:
                                    address = Address(**address_dict)
                                    self.db.add(address)
                                    self.db.flush()
                                    address_id = address.id
                            
                            if address_id:
                                member_dict['address_id'] = address_id
                            member = Member(**member_dict)
                            self.db.add(member)
                            self.db.flush()
                            created_count["members"] += 1
                            
                            # Criar canais de contato se fornecidos
                            if member_data.contact_channels:
                                for channel_data in member_data.contact_channels:
                                    channel_dict = channel_data.dict(exclude_unset=True)
                                    if channel_dict:
                                        channel_dict['member_id'] = member.id
                                        channel = ContactChannel(**channel_dict)
                                        self.db.add(channel)
                            
                            # Criar informações adicionais se fornecidas
                            if member_data.additional_info:
                                additional_dict = member_data.additional_info.dict(exclude_unset=True)
                                if additional_dict:
                                    additional_dict['member_id'] = member.id
                                    additional_info = AdditionalInfo(**additional_dict)
                                    self.db.add(additional_info)

                            # Vincular novo membro às empresas processadas (evitar duplicatas)
                            if processed_company_ids:
                                for company_id in processed_company_ids:
                                    existing_relation = self.db.query(MemberCompany).filter(
                                        and_(
                                            MemberCompany.member_id == member.id,
                                            MemberCompany.company_id == company_id
                                        )
                                    ).first()
                                    if not existing_relation:
                                        self.db.add(MemberCompany(
                                            member_id=member.id,
                                            company_id=company_id,
                                            created_at=datetime.utcnow()
                                        ))
                    except Exception as e:
                        errors.append(f"Erro ao processar membro {member_data.name}: {str(e)}")
            
            # Upsert Performances
            if filtered_data.get("performances"):
                created_count["performances"] = 0
                updated_count["performances"] = 0
                
                for perf_data in filtered_data["performances"]:
                    try:
                        # Criar nova performance (já filtrado, então sempre tem dados)
                        perf_dict = perf_data.dict(exclude_unset=True)
                        
                        # Validar foreign keys antes de criar
                        if 'company_id' in perf_dict and perf_dict['company_id']:
                            if not self._validate_foreign_key(Company, 'id', perf_dict['company_id']):
                                errors.append(f"Company ID {perf_dict['company_id']} não existe")
                                continue
                        
                        performance = Performance(**perf_dict)
                        self.db.add(performance)
                        created_count["performances"] += 1
                    except Exception as e:
                        errors.append(f"Erro ao processar performance: {str(e)}")
            
            # Commit seguro com tratamento de erros
            self._safe_commit()
            
            return {
                "created_count": created_count,
                "updated_count": updated_count,
                "errors": errors,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Erro ao processar dados: {str(e)}")
    
    # ==================== MARKET SEGMENTATIONS ====================
    
    def list_market_segmentations(self) -> List[MarketSegmentation]:
        """Lista todas as segmentações de mercado."""
        return self.db.query(MarketSegmentation).all()
    
    def get_market_segmentation(self, segmentation_id: int) -> Optional[MarketSegmentation]:
        """Busca uma segmentação de mercado por ID."""
        return self.db.query(MarketSegmentation).filter(MarketSegmentation.id == segmentation_id).first()
    
    def create_market_segmentation(self, segmentation_data: MarketSegmentationCreateDTO) -> MarketSegmentation:
        """Cria uma nova segmentação de mercado."""
        # Verificar se já existe por nome
        existing = self.db.query(MarketSegmentation).filter(
            MarketSegmentation.name == segmentation_data.name
        ).first()
        
        if existing:
            raise ValueError(f"Segmentação de mercado com nome '{segmentation_data.name}' já existe")
        
        segmentation = MarketSegmentation(
            name=segmentation_data.name,
            created_at=datetime.utcnow()
        )
        
        self.db.add(segmentation)
        self._safe_commit()
        return segmentation
    
    def update_market_segmentation(self, segmentation_id: int, segmentation_data: MarketSegmentationUpdateDTO) -> Optional[MarketSegmentation]:
        """Atualiza uma segmentação de mercado."""
        segmentation = self.get_market_segmentation(segmentation_id)
        if not segmentation:
            return None
        
        # Verificar se o novo nome já existe (se fornecido)
        if segmentation_data.name and segmentation_data.name != segmentation.name:
            existing = self.db.query(MarketSegmentation).filter(
                MarketSegmentation.name == segmentation_data.name
            ).first()
            
            if existing:
                raise ValueError(f"Segmentação de mercado com nome '{segmentation_data.name}' já existe")
        
        # Atualizar campos
        if segmentation_data.name is not None:
            segmentation.name = segmentation_data.name
            segmentation.updated_at = datetime.utcnow()
        
        self._safe_commit()
        return segmentation
    
    def delete_market_segmentation(self, segmentation_id: int) -> bool:
        """Remove uma segmentação de mercado."""
        segmentation = self.get_market_segmentation(segmentation_id)
        if not segmentation:
            return False
        
        self.db.delete(segmentation)
        self._safe_commit()
        return True
    
    def create_multiple_market_segmentations(self, segmentations_data: List[MarketSegmentationCreateDTO]) -> dict:
        """Cria múltiplas segmentações de mercado."""
        created_segmentations = []
        errors = []
        
        for seg_data in segmentations_data:
            try:
                # Verificar se já existe por nome
                existing = self.db.query(MarketSegmentation).filter(
                    MarketSegmentation.name == seg_data.name
                ).first()
                
                if existing:
                    errors.append(f"Segmentação '{seg_data.name}' já existe")
                    continue
                
                segmentation = MarketSegmentation(
                    name=seg_data.name,
                    created_at=datetime.utcnow()
                )
                
                self.db.add(segmentation)
                created_segmentations.append(segmentation)
                
            except Exception as e:
                errors.append(f"Erro ao criar segmentação '{seg_data.name}': {str(e)}")
        
        if created_segmentations:
            self._safe_commit()
        
        return {
            "created_segmentations": created_segmentations,
            "created_count": len(created_segmentations),
            "errors": errors
        }
