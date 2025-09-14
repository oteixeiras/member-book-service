from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.services.member_service import MemberService
from app.dto.member_dto import MemberResponseDTO, MemberCreateDTO, MemberUpdateDTO
from app.dto.upsert_data_dto import (
    UpsertDataRequestDTO,
    UpsertDataResponseDTO
)
from app.dto.market_segmentation_dto import (
    MarketSegmentationCreateDTO, 
    MarketSegmentationUpdateDTO, 
    MarketSegmentationResponseDTO,
    MarketSegmentationListResponseDTO,
    MarketSegmentationCreateRequestDTO,
    MarketSegmentationCreateResponseDTO
)


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
    
    async def upsert_data(self, request_data: UpsertDataRequestDTO) -> UpsertDataResponseDTO:
        """
        Cria ou atualiza dados do sistema.
        Suporta upsert de todas as tabelas relacionadas.
        """
        try:
            result = await self.member_service.upsert_data(request_data)
            
            return UpsertDataResponseDTO(
                message="Dados processados com sucesso!",
                status="success",
                data=result,
                created_count=result.get("created_count", {}),
                updated_count=result.get("updated_count", {}),
                errors=result.get("errors", [])
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar dados: {str(e)}"
            )
    
    # ==================== MARKET SEGMENTATIONS ====================
    
    async def list_market_segmentations(self) -> MarketSegmentationListResponseDTO:
        """Lista todas as segmentações de mercado."""
        try:
            segmentations = self.member_service.list_market_segmentations()
            
            return MarketSegmentationListResponseDTO(
                message="Segmentações de mercado listadas com sucesso!",
                status="success",
                data=[MarketSegmentationResponseDTO.from_orm(seg) for seg in segmentations],
                total=len(segmentations)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao listar segmentações: {str(e)}"
            )
    
    async def get_market_segmentation(self, segmentation_id: int) -> MarketSegmentationResponseDTO:
        """Busca uma segmentação de mercado por ID."""
        try:
            segmentation = self.member_service.get_market_segmentation(segmentation_id)
            if not segmentation:
                raise HTTPException(status_code=404, detail="Segmentação de mercado não encontrada")
            
            return MarketSegmentationResponseDTO.from_orm(segmentation)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar segmentação: {str(e)}"
            )
    
    async def create_market_segmentation(self, segmentation_data: MarketSegmentationCreateDTO) -> MarketSegmentationResponseDTO:
        """Cria uma nova segmentação de mercado."""
        try:
            segmentation = self.member_service.create_market_segmentation(segmentation_data)
            return MarketSegmentationResponseDTO.from_orm(segmentation)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar segmentação: {str(e)}"
            )
    
    async def create_multiple_market_segmentations(self, request_data: MarketSegmentationCreateRequestDTO) -> MarketSegmentationCreateResponseDTO:
        """Cria múltiplas segmentações de mercado."""
        try:
            result = self.member_service.create_multiple_market_segmentations(request_data.market_segmentations)
            
            return MarketSegmentationCreateResponseDTO(
                message="Segmentações de mercado processadas com sucesso!",
                status="success",
                data=[MarketSegmentationResponseDTO.from_orm(seg) for seg in result["created_segmentations"]],
                created_count=result["created_count"],
                errors=result["errors"]
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao criar segmentações: {str(e)}"
            )
    
    async def update_market_segmentation(self, segmentation_id: int, segmentation_data: MarketSegmentationUpdateDTO) -> MarketSegmentationResponseDTO:
        """Atualiza uma segmentação de mercado."""
        try:
            segmentation = self.member_service.update_market_segmentation(segmentation_id, segmentation_data)
            if not segmentation:
                raise HTTPException(status_code=404, detail="Segmentação de mercado não encontrada")
            
            return MarketSegmentationResponseDTO.from_orm(segmentation)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao atualizar segmentação: {str(e)}"
            )
    
    async def delete_market_segmentation(self, segmentation_id: int) -> Dict[str, str]:
        """Remove uma segmentação de mercado."""
        try:
            success = self.member_service.delete_market_segmentation(segmentation_id)
            if not success:
                raise HTTPException(status_code=404, detail="Segmentação de mercado não encontrada")
            
            return {"message": "Segmentação de mercado removida com sucesso"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao remover segmentação: {str(e)}"
            )
