import asyncio
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from security import get_api_key 
from schemas.professors_schema import ProfessorInfo
from database import get_db
from services import professors_services

router = APIRouter(
    prefix="/api/professors",
    tags=["Professors"]
)

@router.get("/active", response_model=List[ProfessorInfo], status_code=status.HTTP_200_OK)
async def read_active_professors(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todos os professores ativos.
    """

    try:
        active_professors = await asyncio.wait_for(
            professors_services.get_active_professors(db), 
            timeout=60.0
            )
        if not active_professors:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum professor ativo encontrado.")
        return active_professors
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar professores ativos.")
    except Exception as e:
        print(f"Erro ao buscar professores ativos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar professores ativos.")

@router.get("/inactive", response_model=List[ProfessorInfo], status_code=status.HTTP_200_OK)
async def read_inactive_professors(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todos os professores inativos.
    """
    try:
        inactive_professors = await asyncio.wait_for(
            professors_services.get_professors_inactive(db),
            timeout=60.0
            )
        if not inactive_professors:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum professor inativo encontrado.")
    
        return inactive_professors
    
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar professores inativos.")
    except Exception as e:
        print(f"Erro ao buscar professores inativos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar professores inativos.")