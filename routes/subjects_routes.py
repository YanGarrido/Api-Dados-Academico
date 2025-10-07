import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from security import authorization_api, get_api_key 
from schemas.subject_schema import SubjectCompleteInfo, SubjectInfo
from database import get_db
from services import subjects_services

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])

@router.get("/", response_model=List[SubjectInfo], summary="Lista todas as disciplinas", responses={
    200:{"description": "Lista de disciplinas retornada com sucesso."},
    404:{"description": "Nenhuma disciplina foi encontrada."},
    500:{"description": "Erro interno ao buscar disciplinas."},
    504:{"description": "Tempo limite excedido ao buscar disciplinas."}
}
)
async def read_subjects(auth = Depends(authorization_api),db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma json com todas as disciplinas.
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
    

@router.get("/{id}", response_model=SubjectCompleteInfo, summary="Detalhes de uma disciplina específica", responses={
    200:{"description": "Detalhes da disciplina retornados com sucesso."},
    404:{"description": "Disciplina não encontrada."},
    500:{"description": "Erro interno ao buscar disciplina."},
    504:{"description": "Tempo limite excedido ao buscar disciplina."}
})
async def get_subject_by_id(id: str, auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma json com as informações de uma disciplina específica.
    """
    try:       
        subject = await asyncio.wait_for(
            subjects_services.get_complete_subjects(id=id, db=db), 
            timeout=60.0
            )
        
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Disciplina não encontrada.")

        return subject
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail="Tempo limite excedido ao buscar disciplina.")
    except Exception as e:
        print(f"Erro ao buscar disciplina: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro interno ao buscar disciplina.")

@router.get("/current/{periodo_id}", response_model=List[SubjectInfo], summary="Lista disciplinas do semestre atual para múltiplos cursos", responses={
    200:{"description": "Lista de disciplinas retornada com sucesso."},
    400:{"description": "Pelo menos um código de curso deve ser informado."},
    404:{"description": "Nenhuma disciplina encontrada para os cursos informados."},
    500:{"description": "Erro interno ao buscar disciplinas."},
    504:{"description": "Tempo limite excedido ao buscar disciplinas."}
})
async def get_subjects_current_semester(
    periodo_id: int,
    codcurso: str = Query(..., description="Códigos de curso separados por vírgula", example="1,2,4,5,6,10,22"),
    auth = Depends(authorization_api), 
    db: Session = Depends(get_db), 
    api_key: str = Depends(get_api_key)
):
    """
    Retorna disciplinas do semestre atual para múltiplos cursos.
    """
    try:
        codcurso_list = [
            curso.strip().strip('"').strip("'") 
            for curso in codcurso.split(",") 
            if curso.strip()
        ]
        
        if not codcurso_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pelo menos um código de curso deve ser informado"
            )

        subjects = await asyncio.wait_for(
            subjects_services.get_subjects_current_semester(
                codcursos=codcurso_list, 
                periodo_id=periodo_id, 
                db=db
            ),
            timeout=60.0
        )

        if not subjects:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Nenhuma disciplina encontrada para os cursos informados"
            )
        return subjects
     
    except Exception as e:
        print(f"Erro ao buscar disciplinas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao buscar disciplinas"
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
            detail="Tempo limite excedido ao buscar disciplinas"
        )