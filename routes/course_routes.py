import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import get_api_key 
from schemas.course_schema import ClassInfo, CourseInfo, CourseWithSubjects, HasTurmaOut
from database import get_db
from services import course_services

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseInfo])
async def read_courses(db: Session = Depends(get_db),api_key: str = Depends(get_api_key) ):
    """
    Retorna uma lista de todos os cursos.
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

@router.get("/{course_id}", response_model=CourseWithSubjects, status_code=status.HTTP_200_OK)
async def get_course_with_subjects(course_id: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Retorna os detalhes de um curso específico, incluindo uma lista 
    com os nomes de todas as disciplinas desse curso.
    """

    course_details = await course_services.get_course_with_subjects(course_id=course_id, db=db)

    if not course_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Curso com código '{course_id}' não encontrado.")
    return course_details

@router.get("/{codcurso}/{codturno}/{periodoletivo_id}/{periodo}/temTurma", response_model=HasTurmaOut)
async def has_class_period(codcurso: str,codturno: int, periodoletivo_id: int, periodo: int, db:Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    class_details = await course_services.has_class_period(codcurso=codcurso,codturno=codturno,periodoletivo_id=periodoletivo_id, periodo=periodo,db=db)

    if not class_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f"Erro ao realizar requisição"))
    return class_details

@router.get("/class/active/{periodo_letivo_id}/{periodo}/{codturno}", response_model=List[ClassInfo])
async def semester_class_active(periodo_letivo_id: int, periodo: int, codturno: int, db:Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    class_details = await course_services.semester_class_active(periodo_letivo_id=periodo_letivo_id, periodo=periodo, codturno=codturno, db=db)

    if not class_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=("Não foi possivel localizar turmas ativas nesse semestre"))
    return class_details

