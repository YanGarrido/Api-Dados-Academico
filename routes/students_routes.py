import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import get_api_key 
from schemas.students_schema import StudentInfo, StudentWithCourses
from database import get_db
from services import students_services

router = APIRouter(
    prefix="/api/students", 
    tags=["Students"])

@router.get("/active", response_model=List[StudentInfo], status_code=status.HTTP_200_OK)
async def read_active_students(db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todos os alunos ativos.
    """
    try:
        active_students = await asyncio.wait_for(
        students_services.get_active_students(db), 
        timeout=60.0
        )
        if not active_students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum aluno ativo encontrado.")
        return active_students
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar alunos ativos.")
    except Exception as e:
        print(f"Erro ao buscar alunos ativos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar alunos ativos.")

@router.get("/inactive", response_model=List[StudentInfo], status_code=status.HTTP_200_OK)
async def read_inactive_students(db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todos os alunos inativos.
    """
    try:
        inactive_students = await asyncio.wait_for(
        students_services.get_inactive_students(db),
        timeout=60.0
        )
        if not inactive_students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum aluno inativo encontrado.")
        return inactive_students
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar alunos inativos.")
    except Exception as e:
        print(f"Erro ao buscar alunos inativos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar alunos inativos.")

@router.get("/former", response_model=List[StudentInfo], status_code=status.HTTP_200_OK)
async def read_former_students(db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma lista de todos os alunos ex-alunos.
    """
    try:
        former_students = await asyncio.wait_for(
        students_services.get_former_students(db), timeout=60.0)
        if not former_students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum ex-aluno encontrado.")
        return former_students
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar ex-alunos.")
    except Exception as e:
        print(f"Erro ao buscar ex-alunos: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar ex-alunos.")

@router.get("/active/{ra}", response_model=StudentInfo, status_code=status.HTTP_200_OK)
async def read_active_student_by_ra(ra: str, db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna informações de um aluno ativo pelo RA.
    """
    try:
        if not ra:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="RA não pode ser vazio.")
        
        student = await asyncio.wait_for(
            students_services.get_active_student_by_ra(ra, db), 
            timeout=60.0
        )
        if not student:
            raise HTTPException(status_code=404, detail="Aluno não encontrado ou não está ativo.")
        return student
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar aluno ativo pelo RA.")
    except Exception as e:
        print(f"Erro ao buscar aluno ativo pelo RA: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar aluno ativo pelo RA.")  
    
@router.get("/active/courses/{ra}", response_model=StudentWithCourses, status_code=status.HTTP_200_OK)
async def read_active_student_with_course(ra: str, db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    try:
        if not ra:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="RA não pode ser vazio.")
        
        student = await asyncio.wait_for(
            students_services.get_active_student_with_course(ra, db), 
            timeout=60.0
        )
        if not student:
            raise HTTPException(status_code=404, detail="Aluno não encontrado ou não está ativo.")
        return student
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar aluno ativo pelo RA.")
    except Exception as e:
        print(f"Erro ao buscar aluno ativo pelo RA: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar aluno ativo pelo RA.")  