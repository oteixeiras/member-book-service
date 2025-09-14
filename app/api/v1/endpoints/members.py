from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.controllers.member_controller import MemberController
from app.dto.member_dto import (
    MemberResponseDTO, 
    MemberCreateDTO, 
    MemberUpdateDTO, 
    MemberListResponseDTO,
    MemberSearchDTO
)
from typing import Dict, Any

router = APIRouter()


@router.put("/populate-data", response_model=Dict[str, Any])
async def populate_data(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Endpoint para popular ou atualizar dados iniciais.
    Atualmente popula a tabela profiles com dados padrão.
    """
    controller = MemberController(db)
    return await controller.populate_data()


@router.get("/", response_model=MemberListResponseDTO)
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


@router.get("/{member_id}", response_model=MemberResponseDTO)
async def get_member(
    member_id: int,
    db: Session = Depends(get_db)
) -> MemberResponseDTO:
    """
    Busca um membro pelo ID.
    """
    controller = MemberController(db)
    return await controller.get_member(member_id)


@router.post("/", response_model=MemberResponseDTO)
async def create_member(
    member_data: MemberCreateDTO,
    db: Session = Depends(get_db)
) -> MemberResponseDTO:
    """
    Cria um novo membro.
    """
    controller = MemberController(db)
    return await controller.create_member(member_data)


@router.put("/{member_id}", response_model=MemberResponseDTO)
async def update_member(
    member_id: int,
    member_data: MemberUpdateDTO,
    db: Session = Depends(get_db)
) -> MemberResponseDTO:
    """
    Atualiza um membro existente.
    """
    controller = MemberController(db)
    return await controller.update_member(member_id, member_data)


@router.delete("/{member_id}", response_model=Dict[str, str])
async def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Remove um membro.
    """
    controller = MemberController(db)
    return await controller.delete_member(member_id)
