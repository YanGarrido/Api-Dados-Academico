import asyncio
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.subject_schema import SubjectInfo
from security import authorization_api, get_api_key 
from schemas.professors_schema import ProfessorInfo, ProfessorWithSubjects
from database import get_db
from services import professors_services

router = APIRouter(
    prefix="/api/professors",
    tags=["Professors"]
)

@router.get("/active", response_model=List[ProfessorInfo], status_code=status.HTTP_200_OK)
async def read_active_professors(auth = Depends(authorization_api),db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
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
async def read_inactive_professors(auth = Depends(authorization_api),db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
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
    
@router.get("/{professor_code}", 
    response_model=ProfessorWithSubjects, status_code=status.HTTP_200_OK, summary="Busca um professor e suas disciplinas"
)
async def get_professor_with_subjects(professor_code: str,auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna os detalhes de um professor específico, incluindo uma lista
    com os nomes de todas as disciplinas que ele leciona.
    """
    # A sua lógica de serviço que busca os dados está correta
    professor_details = await professors_services.get_professors_with_subjects(codigo_professor=professor_code, db=db)
    
    if not professor_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"Professor com código '{professor_code}' não encontrado."))
        
    return professor_details

@router.get("/active/{codcurso}/{periodo_id}", response_model=List[ProfessorInfo], status_code=status.HTTP_200_OK)
async def get_professor_still_active(codcurso: str, periodo_id: int,auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna os detalhes de um professor específico que lecionava em semestres anteriores e que continua ativo
    """

    professor_details = await professors_services.get_professor_still_active(codcurso=codcurso, periodo_id=periodo_id, db=db)

    if not professor_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"Professores não encontrados"))
    
    return professor_details