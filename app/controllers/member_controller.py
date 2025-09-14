from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.services.member_service import MemberService
from app.dto.member_dto import MemberResponseDTO, MemberCreateDTO, MemberUpdateDTO


class MemberController:
    """Controller responsável por gerenciar as operações relacionadas aos membros."""
    
    def __init__(self, db: Session):
        self.member_service = MemberService(db)
    
    async def populate_data(self) -> Dict[str, Any]:
        """
        Popula ou atualiza dados iniciais.
        Atualmente popula a tabela profiles com dados padrão.
        """
        try:
            result = await self.member_service.populate_initial_data()
            
            return {
                "message": "Dados populados com sucesso!",
                "status": "success",
                "data": result
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao popular dados: {str(e)}"
            )
    
    async def get_member(self, member_id: int) -> MemberResponseDTO:
        """Busca um membro pelo ID."""
        try:
            member = await self.member_service.get_member_by_id(member_id)
            if not member:
                raise HTTPException(status_code=404, detail="Membro não encontrado")
            
            return MemberResponseDTO.from_orm(member)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar membro: {str(e)}"
            )
    
    async def create_member(self, member_data: MemberCreateDTO) -> MemberResponseDTO:
        """Cria um novo membro."""
        try:
            member = await self.member_service.create_member(member_data)
            return MemberResponseDTO.from_orm(member)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao criar membro: {str(e)}"
            )
    
    async def update_member(self, member_id: int, member_data: MemberUpdateDTO) -> MemberResponseDTO:
        """Atualiza um membro existente."""
        try:
            member = await self.member_service.update_member(member_id, member_data)
            if not member:
                raise HTTPException(status_code=404, detail="Membro não encontrado")
            
            return MemberResponseDTO.from_orm(member)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao atualizar membro: {str(e)}"
            )
    
    async def delete_member(self, member_id: int) -> Dict[str, str]:
        """Remove um membro."""
        try:
            success = await self.member_service.delete_member(member_id)
            if not success:
                raise HTTPException(status_code=404, detail="Membro não encontrado")
            
            return {"message": "Membro removido com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao remover membro: {str(e)}"
            )
    
    async def list_members(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Lista membros com paginação."""
        try:
            members, total = await self.member_service.list_members(skip, limit)
            
            return {
                "members": [MemberResponseDTO.from_orm(member) for member in members],
                "total": total,
                "skip": skip,
                "limit": limit
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao listar membros: {str(e)}"
            )
