from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from app.models.member import MemberStatusEnum


class MemberBaseDTO(BaseModel):
    """DTO base para membros."""
    name: str = Field(..., min_length=1, max_length=255, description="Nome do membro")
    position: Optional[str] = Field(None, max_length=255, description="Cargo do membro")
    biography: Optional[str] = Field(None, description="Biografia do membro")
    document: str = Field(..., min_length=11, max_length=14, description="CPF do membro")
    photo_url: Optional[str] = Field(None, description="URL da foto do membro")
    address_id: Optional[int] = Field(None, description="ID do endereço")
    status: MemberStatusEnum = Field(MemberStatusEnum.pending, description="Status do membro")
    expired_at: Optional[date] = Field(None, description="Data de expiração do acesso")
    profile_id: Optional[int] = Field(None, description="ID do perfil")
    
    @validator('document')
    def validate_document(cls, v):
        """Valida o formato do CPF."""
        # Remove caracteres não numéricos
        document = ''.join(filter(str.isdigit, v))
        
        if len(document) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        
        # Validação básica de CPF
        if document == document[0] * 11:
            raise ValueError('CPF inválido')
        
        return document


class MemberCreateDTO(MemberBaseDTO):
    """DTO para criação de membros."""
    pass


class MemberUpdateDTO(BaseModel):
    """DTO para atualização de membros."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nome do membro")
    position: Optional[str] = Field(None, max_length=255, description="Cargo do membro")
    biography: Optional[str] = Field(None, description="Biografia do membro")
    document: Optional[str] = Field(None, min_length=11, max_length=14, description="CPF do membro")
    photo_url: Optional[str] = Field(None, description="URL da foto do membro")
    address_id: Optional[int] = Field(None, description="ID do endereço")
    status: Optional[MemberStatusEnum] = Field(None, description="Status do membro")
    expired_at: Optional[date] = Field(None, description="Data de expiração do acesso")
    profile_id: Optional[int] = Field(None, description="ID do perfil")
    
    @validator('document')
    def validate_document(cls, v):
        """Valida o formato do CPF."""
        if v is None:
            return v
            
        # Remove caracteres não numéricos
        document = ''.join(filter(str.isdigit, v))
        
        if len(document) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        
        # Validação básica de CPF
        if document == document[0] * 11:
            raise ValueError('CPF inválido')
        
        return document


class MemberResponseDTO(BaseModel):
    """DTO para resposta de membros."""
    id: int
    name: str
    position: Optional[str]
    biography: Optional[str]
    document: str
    photo_url: Optional[str]
    address_id: Optional[int]
    status: MemberStatusEnum
    expired_at: Optional[date]
    profile_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MemberListResponseDTO(BaseModel):
    """DTO para resposta de lista de membros."""
    members: list[MemberResponseDTO]
    total: int
    skip: int
    limit: int


class MemberSearchDTO(BaseModel):
    """DTO para busca de membros."""
    name: Optional[str] = Field(None, description="Nome do membro")
    status: Optional[MemberStatusEnum] = Field(None, description="Status do membro")
    profile_id: Optional[int] = Field(None, description="ID do perfil")
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")
