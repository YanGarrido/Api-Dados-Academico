import asyncio
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.subject_schema import SubjectInfo
from security import authorization_api, get_api_key 
from schemas.professors_schema import ProfessorInfo, ProfessorWithSubjects
from database import get_db
from services import professors_services

router = APIRouter(prefix="/api/professors", tags=["Professors"])

@router.get("/active", response_model=List[ProfessorInfo], summary="Lista todos os professores ativos", responses={
    200:{"description": "Lista de professores ativos retornada com sucesso."},
    404:{"description": "Nenhum professor ativo foi encontrado."},
    500:{"description": "Erro interno ao buscar professores ativos."},
    504:{"description": "Tempo limite excedido ao buscar professores ativos."}
}
)
async def read_active_professors(auth = Depends(authorization_api),db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma json de todos os professores ativos.
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

@router.get("/inactive", response_model=List[ProfessorInfo], summary="Lista todos os professores inativos", responses={
    200:{"description": "Lista de professores inativos retornada com sucesso."},
    404:{"description": "Nenhum professor inativo foi encontrado."},
    500:{"description": "Erro interno ao buscar professores inativos."},
    504:{"description": "Tempo limite excedido ao buscar professores inativos."}
}
)
async def read_inactive_professors(auth = Depends(authorization_api),db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma json de todos os professores inativos.
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
    response_model=ProfessorWithSubjects, summary="Busca um professor e suas disciplinas", responses={
    200:{"description": "Detalhes do professor retornados com sucesso."},
    404:{"description": "Professor não encontrado."},
    500:{"description": "Erro interno ao buscar professor."},
    504:{"description": "Tempo limite excedido ao buscar professor."}
})
async def get_professor_with_subjects(professor_code: str,auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna os detalhes de um professor específico, incluindo uma lista com os nomes de todas as disciplinas que ele leciona.
    """
    try:
        professor_details = await asyncio.wait_for(
            professors_services.get_professors_with_subjects(codigo_professor=professor_code, db=db), 
            timeout=60.0
            )
        
        if not professor_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Professor com código '{professor_code}' não encontrado.")
        
        return professor_details
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail="Tempo limite excedido ao buscar professor.")
    except Exception as e:
        print(f"Erro ao buscar professor: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro interno ao buscar professor.")

@router.get("/active/{codcurso}/{periodo_letivo_id}", response_model=List[ProfessorInfo], summary="Lista professores que lecionavam em semestres anteriores e que continuam ativos", responses={
    200:{"description": "Lista de professores retornada com sucesso."},
    404:{"description": "Nenhum professor encontrado."},
    500:{"description": "Erro interno ao buscar professores."},
    504:{"description": "Tempo limite excedido ao buscar professores."}
})
async def get_professor_still_active(codcurso: str, periodo_letivo_id: int,auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna os detalhes de um professor específico que lecionava em semestres anteriores e que continua ativo
    """
    try:
        professor_details = await asyncio.wait_for(
            professors_services.get_professor_still_active(codcurso=codcurso, periodo_letivo_id=periodo_letivo_id, db=db), 
            timeout=60.0
            )

        if not professor_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"Professores não encontrados"))
    
        return professor_details
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail="Tempo limite excedido ao buscar professores.")
    except Exception as e:
        print(f"Erro ao buscar professores: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro interno ao buscar professores.")