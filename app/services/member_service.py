from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, Tuple, List
from app.models.member import Member
from app.dto.member_dto import MemberCreateDTO, MemberUpdateDTO
from app.seeds.profiles_seed import seed_profiles
from datetime import datetime


class MemberService:
    """Service responsável pela lógica de negócio relacionada aos membros."""
    
    def __init__(self, db: Session):
        self.db = db
    
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
