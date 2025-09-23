import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import get_api_key 
from schemas.subject_schema import SubjectCompleteInfo, SubjectInfo
from database import get_db
from services import subjects_services

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])

@router.get("/", response_model=List[SubjectInfo])
async def read_subjects(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todas as disciplinas.
    """
    try:
        subjects = await asyncio.wait_for(
            subjects_services.get_all_subjects(db), 
            timeout=60.0
            )
        if not subjects:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhuma disciplina encontrada.")
        return subjects
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar disciplinas.")
    except Exception as e:
        print(f"Erro ao buscar disciplinas: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar disciplinas.")
    

@router.get("/{id}", response_model=SubjectCompleteInfo)
async def get_subject_by_id(id: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    subject = await subjects_services.get_complete_subjects(id=id, db=db)
    
    if not subject:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return subject

@router.get("/current/{codcurso}/{periodo_id}", response_model=List[SubjectInfo])
async def get_subjects_current_semester(codcurso: str, periodo_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
     subject = await subjects_services.get_subjects_current_semester(codcurso=codcurso, periodo_id=periodo_id, db=db)

     if not subject:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
     return subject