import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import authorization_api, get_api_key 
from schemas.course_schema import ClassInfo, CourseInfo, CourseWithSubjects, HasTurmaOut
from database import get_db
from services import course_services

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseInfo],summary="Lista todos os cursos",responses={
    200:{"description": "Lista de cursos retornada com sucesso."},
    404:{"description": "Nenhum curso foi encontrado."},
    500:{"description": "Erro interno ao buscar cursos."},
    504:{"description": "Tempo limite excedido ao buscar cursos."}
}
)
async def read_courses(auth = Depends(authorization_api),db: Session = Depends(get_db),api_key: str = Depends(get_api_key)):
    """
    Rota que busca no banco de dados todos os cursos disponíveis e retorna uma lista com as informações básicas de cada curso, como código e nome.
    """
    try:
        courses = await asyncio.wait_for(
            course_services.get_all_courses(db), 
            timeout=60.0
            )
        
        if not courses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum curso encontrado.")
        
        return courses
    
    except asyncio.TimeoutError:
        
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar cursos.")
    
    except Exception as e:
        
        print(f"Erro ao buscar cursos: {e}")
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar cursos.")

@router.get("/{codcurso}", response_model=CourseWithSubjects,summary="Detalhes de um curso específico",responses={
    200:{"description": "Detalhes do curso retornados com sucesso."},
    404:{"description": "Curso não encontrado."},
    500:{"description": "Erro interno ao buscar detalhes do curso."},
    504:{"description": "Tempo limite excedido ao buscar detalhes do curso."}
})
async def get_course_with_subjects(codcurso: str, auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna os detalhes de um curso específico, incluindo uma lista 
    com os nomes de todas as disciplinas desse curso.
    """
    try:
        course_details = await asyncio.wait_for(
            course_services.get_course_with_subjects(codcurso=codcurso, db=db), 
            timeout=60.0
            )
        
        if not course_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Curso com código '{codcurso}' não encontrado.")
        
        return course_details

    except asyncio.TimeoutError:

        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar detalhes do curso.")
    
    except Exception as e: 
        
        print(f"Erro ao buscar detalhes do curso: {e}")
        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar detalhes do curso.")


@router.get("/{codcurso}/{codturno}/{periodo_letivo_id}/{periodo}/temTurma", response_model=HasTurmaOut, description="Verifica se há turmas ativas para um curso em um determinado período letivo e turno.", responses={
    200: {"description": "Informações sobre a existência de turmas retornadas com sucesso."},
    404: {"description": "Erro ao realizar requisição."},
    500: {"description": "Erro interno ao verificar turmas."},
    504: {"description": "Tempo limite excedido ao verificar turmas."}
})
async def has_class_period(codcurso: str,codturno: int, periodo_letivo_id: int, periodo: int, auth = Depends(authorization_api), db:Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Verifica se há turmas ativas para um curso em um determinado período letivo e turno."""

    try:
        class_details = await asyncio.wait_for(
            course_services.has_class_period(codcurso=codcurso,codturno=codturno,periodo_letivo_id=periodo_letivo_id, periodo=periodo,db=db),
            timeout=60.0
        )

        if not class_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"Erro ao realizar requisição"))
        return class_details

    except asyncio.TimeoutError:

        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar informações da turma.")

    except Exception as e:

        print(f"Erro ao buscar informações da turma: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar informações da turma.")

@router.get("/class/active/{periodo_letivo_id}/{periodo}/{codturno}", response_model=List[ClassInfo], description="Retorna uma lista de todas as turmas ativas em um semestre específico.", responses={
    200: {"description": "Lista de turmas ativas retornada com sucesso."},
    404: {"description": "Nenhum curso foi encontrado."},
    500: {"description": "Erro interno ao buscar turmas."},
    504: {"description": "Tempo limite excedido ao buscar turmas."}
})
async def semester_class_active(periodo_letivo_id: int, periodo: int, codturno: int, auth = Depends(authorization_api), db:Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todas as turmas ativas em um semestre específico.
    """
    try:
        class_details = await asyncio.wait_for(
            course_services.semester_class_active(periodo_letivo_id=periodo_letivo_id, periodo=periodo, codturno=codturno, db=db),
            timeout=60.0
        )
    
        if not class_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=("Não foi possivel localizar turmas ativas nesse semestre"))
        return class_details

    except asyncio.TimeoutError:

        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar informações das turmas.")

    except Exception as e:

        print(f"Erro ao buscar informações das turmas: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar informações das turmas.")

@router.get("/professors/{codcurso}")
async def get_course_with_professors(codcurso: str, auth = Depends(authorization_api), db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    try:
        course_details = await asyncio.wait_for(
            course_services.get_course_with_professors(codcurso=codcurso, db=db),
            timeout=60.0
        )

        if not course_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=("Não foi possível localizar professores para o curso"))
        return course_details

    except asyncio.TimeoutError:

        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar informações dos professores.")

    except Exception as e:

        print(f"Erro ao buscar informações dos professores: {e}")

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar informações dos professores.")