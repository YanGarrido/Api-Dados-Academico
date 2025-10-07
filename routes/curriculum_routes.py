import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import authorization_api, get_api_key 
from schemas.curriculum_schema import CurriculumInfo
from database import get_db
from services import curriculum_services

router = APIRouter(prefix="/api/curriculums", tags=["Curriculum"])


@router.get("/", response_model=List[CurriculumInfo], summary="Lista todos os currículos", responses={
    200:{"description": "Lista de currículos retornada com sucesso."},
    404:{"description": "Nenhum currículo foi encontrado."},
    500:{"description": "Erro interno ao buscar currículos."},
    504:{"description": "Tempo limite excedido ao buscar currículos."}
}
)
async def read_curriculum(auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna a grade curricular de todos os cursos disponíveis.
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

@router.get("/{curso}", response_model=List[CurriculumInfo], summary="Currículo de um curso específico", responses={
    200:{"description": "Currículo retornado com sucesso."},
    404:{"description": "Nenhum currículo encontrado."},
    500:{"description": "Erro interno ao buscar currículo."},
    504:{"description": "Tempo limite excedido ao buscar currículo."}
})
async def read_curriculum_course(curso: str, auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna a grade curricular de um curso específico.
    """
    try:
        curriculum = await asyncio.wait_for(
            curriculum_services.get_curriculum_current_course(curso,db), 
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
    
@router.get("/old/{curso}", response_model=List[CurriculumInfo], summary="Currículo antigo de um curso específico", responses={
    200:{"description": "Currículo antigo retornado com sucesso."},
    404:{"description": "Nenhum currículo antigo encontrado."},
    500:{"description": "Erro interno ao buscar currículo antigo."},
    504:{"description": "Tempo limite excedido ao buscar currículo antigo."}
})
async def read_old_curriculum(curso: str, auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna a grade curricular antiga de um curso específico.
    """
    try:
        curriculum = await asyncio.wait_for(
            curriculum_services.get_old_curriculum(curso,db), 
            timeout=60.0
        )
        if not curriculum:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum currículo antigo encontrado.")
        return curriculum
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar currículo antigo.")
    except Exception as e:
        print(f"Erro ao buscar currículo antigo: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar currículo antigo.")