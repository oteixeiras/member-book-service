from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from app.models.member import MemberStatusEnum
from app.models.address import StateEnum
from app.models.contact_channel import ContactChannelTypeEnum
from app.models.profile import ProfileTypeEnum


class AddressUpsertDTO(BaseModel):
    """DTO para upsert de endereço."""
    street: Optional[str] = Field(None, description="Rua")
    number: Optional[str] = Field(None, description="Número")
    complement: Optional[str] = Field(None, description="Complemento")
    neighborhood: Optional[str] = Field(None, description="Bairro")
    city: Optional[str] = Field(None, description="Cidade")
    state: Optional[StateEnum] = Field(None, description="Estado")
    country: Optional[str] = Field("Brazil", description="País")
    postal_code: Optional[str] = Field(None, description="CEP")


class ContactChannelUpsertDTO(BaseModel):
    """DTO para upsert de canal de contato."""
    type: Optional[ContactChannelTypeEnum] = Field(None, description="Tipo do canal de contato")
    content: Optional[str] = Field(None, description="Conteúdo do contato")


class AdditionalInfoUpsertDTO(BaseModel):
    """DTO para upsert de informações adicionais."""
    hobby: Optional[str] = Field(None, description="Hobby")
    role_duration: Optional[int] = Field(None, description="Tempo de trabalho em meses")
    children_count: Optional[int] = Field(None, description="Número de filhos")


class MarketSegmentationUpsertDTO(BaseModel):
    """DTO para upsert de segmentação de mercado."""
    name: Optional[str] = Field(None, description="Nome da segmentação")


class CompanyUpsertDTO(BaseModel):
    """DTO para upsert de empresa."""
    name: Optional[str] = Field(None, description="Nome da empresa")
    document: Optional[str] = Field(None, description="CNPJ da empresa")
    founded_year: Optional[date] = Field(None, description="Ano de fundação")
    market_segmentation_id: Optional[int] = Field(None, description="ID da segmentação de mercado")
    address: Optional[AddressUpsertDTO] = Field(None, description="Endereço da empresa")


class PerformanceUpsertDTO(BaseModel):
    """DTO para upsert de performance."""
    count_closed_deals: Optional[int] = Field(None, description="Quantidade de negócios fechados")
    value_closed_deals: Optional[int] = Field(None, description="Valor dos negócios fechados")
    referrals_received: Optional[int] = Field(None, description="Quantidade de indicações recebidas")
    total_value_per_referral: Optional[int] = Field(None, description="Valor total por indicações")
    referrals_given: Optional[int] = Field(None, description="Quantidade de indicações fornecidas")


class MemberUpsertDTO(BaseModel):
    """DTO para upsert de membro."""
    name: Optional[str] = Field(None, description="Nome do membro")
    position: Optional[str] = Field(None, description="Cargo do membro")
    biography: Optional[str] = Field(None, description="Biografia do membro")
    document: Optional[str] = Field(None, description="CPF do membro")
    photo_url: Optional[str] = Field(None, description="URL da foto do membro")
    status: Optional[MemberStatusEnum] = Field(None, description="Status do membro")
    expired_at: Optional[date] = Field(None, description="Data de expiração do acesso")
    profile_id: Optional[int] = Field(None, description="ID do perfil")
    
    # Dados relacionados
    address: Optional[AddressUpsertDTO] = Field(None, description="Endereço do membro")
    contact_channels: Optional[List[ContactChannelUpsertDTO]] = Field(None, description="Canais de contato")
    additional_info: Optional[AdditionalInfoUpsertDTO] = Field(None, description="Informações adicionais")


class UpsertDataRequestDTO(BaseModel):
    """DTO para requisição de upsert de dados."""
    # Companies
    companies: Optional[List[CompanyUpsertDTO]] = Field(None, description="Empresas")
    
    # Members
    members: Optional[List[MemberUpsertDTO]] = Field(None, description="Membros")
    
    # Performances (relacionadas às empresas)
    performances: Optional[List[PerformanceUpsertDTO]] = Field(None, description="Performances")
    
    def get_non_empty_objects(self) -> dict:
        """Retorna apenas objetos que possuem pelo menos um campo populado."""
        result = {}
        
        # Companies - filtrar objetos não vazios
        if self.companies:
            non_empty_companies = [
                comp for comp in self.companies 
                if any(comp.dict(exclude_unset=True, exclude={'address'}).values()) or 
                   (comp.address and any(comp.address.dict(exclude_unset=True).values()))
            ]
            if non_empty_companies:
                result["companies"] = non_empty_companies
        
        # Members - filtrar objetos não vazios
        if self.members:
            non_empty_members = [
                member for member in self.members 
                if any(member.dict(exclude_unset=True, exclude={'address', 'contact_channels', 'additional_info'}).values()) or
                   (member.address and any(member.address.dict(exclude_unset=True).values())) or
                   (member.contact_channels and any(
                       any(ch.dict(exclude_unset=True).values()) for ch in member.contact_channels
                   )) or
                   (member.additional_info and any(member.additional_info.dict(exclude_unset=True).values()))
            ]
            if non_empty_members:
                result["members"] = non_empty_members
        
        # Performances - filtrar objetos não vazios
        if self.performances:
            non_empty_perfs = [
                perf for perf in self.performances 
                if any(perf.dict(exclude_unset=True).values())
            ]
            if non_empty_perfs:
                result["performances"] = non_empty_perfs
        
        return result


class UpsertDataResponseDTO(BaseModel):
    """DTO para resposta de upsert de dados."""
    message: str
    status: str
    data: dict
    created_count: dict
    updated_count: dict
    errors: List[str] = []
