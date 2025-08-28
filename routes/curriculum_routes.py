import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.curriculum_schema import CurriculumInfo
from database import get_db
from services import curriculum_services

router = APIRouter(prefix="/api/curriculums", tags=["Curriculum"])

@router.get("/", response_model=List[CurriculumInfo])
async def read_curriculum(db: Session = Depends(get_db)):
    """
    Retorna o currículo de um curso específico.
    """
    try:
        curriculum = await asyncio.wait_for(
            curriculum_services.get_curriculum(db), 
            timeout=60.0
        )
        if not curriculum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum currículo encontrado.")
        return curriculum
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar currículo.")
    except Exception as e:
        print(f"Erro ao buscar currículo: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar currículo.")