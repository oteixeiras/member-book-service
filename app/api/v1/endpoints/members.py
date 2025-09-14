from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.member_controller import MemberController
from app.dto.member_dto import (
    MemberResponseDTO,
    MemberListResponseDTO
)
from app.dto.upsert_data_dto import (
    UpsertDataRequestDTO,
    UpsertDataResponseDTO
)
from app.dto.market_segmentation_dto import (
    MarketSegmentationCreateRequestDTO,
    MarketSegmentationCreateResponseDTO
)
from typing import Dict, Any

router = APIRouter()


@router.put("/populate-data", response_model=UpsertDataResponseDTO, tags=["Data Management"])
async def upsert_data(
    request_data: UpsertDataRequestDTO,
    db: Session = Depends(get_db)
) -> UpsertDataResponseDTO:
    """
    Endpoint para criar ou atualizar dados do sistema.
    Suporta upsert de: profiles, market_segmentations, companies, members, performances.
    Campos únicos duplicados são ignorados.
    """
    controller = MemberController(db)
    return await controller.upsert_data(request_data)


@router.get("/", response_model=MemberListResponseDTO, tags=["Members"])
async def list_members(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
) -> MemberListResponseDTO:
    """
    Lista todos os membros com paginação.
    """
    controller = MemberController(db)
    result = await controller.list_members(skip, limit)
    return MemberListResponseDTO(**result)


@router.get("/{member_id}", response_model=MemberResponseDTO, tags=["Members"])
async def get_member(
    member_id: int,
    db: Session = Depends(get_db)
) -> MemberResponseDTO:
    """
    Busca um membro pelo ID.
    """
    controller = MemberController(db)
    return await controller.get_member(member_id)


 


@router.delete("/{member_id}", response_model=Dict[str, str], tags=["Members"])
async def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Remove um membro.
    """
    controller = MemberController(db)
    return await controller.delete_member(member_id)


# ==================== MARKET SEGMENTATIONS ENDPOINTS ====================

@router.post("/market-segmentations/bulk", response_model=MarketSegmentationCreateResponseDTO, tags=["Market Segmentations"])
async def create_multiple_market_segmentations(
    request_data: MarketSegmentationCreateRequestDTO,
    db: Session = Depends(get_db)
) -> MarketSegmentationCreateResponseDTO:
    """
    Cria múltiplas segmentações de mercado em lote.
    """
    controller = MemberController(db)
    return await controller.create_multiple_market_segmentations(request_data)
