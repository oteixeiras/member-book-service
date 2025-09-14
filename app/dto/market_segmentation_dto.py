from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MarketSegmentationCreateDTO(BaseModel):
    """DTO para criação de segmentação de mercado."""
    name: str = Field(..., description="Nome da segmentação de mercado")


class MarketSegmentationUpdateDTO(BaseModel):
    """DTO para atualização de segmentação de mercado."""
    name: Optional[str] = Field(None, description="Nome da segmentação de mercado")


class MarketSegmentationResponseDTO(BaseModel):
    """DTO para resposta de segmentação de mercado."""
    id: int = Field(..., description="ID da segmentação")
    name: str = Field(..., description="Nome da segmentação")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")
    
    class Config:
        from_attributes = True


class MarketSegmentationListResponseDTO(BaseModel):
    """DTO para resposta de lista de segmentações."""
    message: str = Field(..., description="Mensagem de resposta")
    status: str = Field(..., description="Status da operação")
    data: List[MarketSegmentationResponseDTO] = Field(..., description="Lista de segmentações")
    total: int = Field(..., description="Total de segmentações")


class MarketSegmentationCreateRequestDTO(BaseModel):
    """DTO para requisição de criação de múltiplas segmentações."""
    market_segmentations: List[MarketSegmentationCreateDTO] = Field(..., description="Lista de segmentações para criar")


class MarketSegmentationCreateResponseDTO(BaseModel):
    """DTO para resposta de criação de segmentações."""
    message: str = Field(..., description="Mensagem de resposta")
    status: str = Field(..., description="Status da operação")
    data: List[MarketSegmentationResponseDTO] = Field(..., description="Segmentações criadas")
    created_count: int = Field(..., description="Quantidade de segmentações criadas")
    errors: List[str] = Field(default_factory=list, description="Lista de erros")
