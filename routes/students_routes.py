import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import authorization_api, get_api_key 
from schemas.students_schema import StudentInfo, StudentWithCourses
from database import get_db
from services import students_services

router = APIRouter(
    prefix="/api/students", 
    tags=["Students"])

@router.get("/active", response_model=List[StudentInfo], summary="Lista todos os alunos ativos", responses={
    200:{"description": "Lista de alunos ativos retornada com sucesso."},
    404:{"description": "Nenhum aluno ativo foi encontrado."},
    500:{"description": "Erro interno ao buscar alunos ativos."},
    504:{"description": "Tempo limite excedido ao buscar alunos ativos."}
}
)
async def read_active_students(auth = Depends(authorization_api),db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma json de todos os alunos que estão ativos.
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

@router.get("/inactive", response_model=List[StudentInfo], summary="Lista todos os alunos inativos", responses={
    200:{"description": "Lista de alunos inativos retornada com sucesso."},
    404:{"description": "Nenhum aluno inativo foi encontrado."},
    500:{"description": "Erro interno ao buscar alunos inativos."},
    504:{"description": "Tempo limite excedido ao buscar alunos inativos."}
}
)
async def read_inactive_students(auth = Depends(authorization_api), db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma json de todos os alunos que estão inativos.
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

@router.get("/former", response_model=List[StudentInfo], summary="Lista todos os ex-alunos", responses={
    200:{"description": "Lista de ex-alunos retornada com sucesso."},
    404:{"description": "Nenhum ex-aluno encontrado."},
    500:{"description": "Erro interno ao buscar ex-alunos."},
    504:{"description": "Tempo limite excedido ao buscar ex-alunos."}
}
)
async def read_former_students(auth = Depends(authorization_api),db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma json de todos os alunos ex-alunos.
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

@router.get("/active/{ra}", response_model=StudentInfo, summary="Busca um aluno ativo pelo RA", responses={
    200:{"description": "Detalhes do aluno retornados com sucesso."},
    400:{"description": "RA não pode ser vazio."},
    404:{"description": "Aluno não encontrado ou não está ativo."},
    500:{"description": "Erro interno ao buscar aluno."},
    504:{"description": "Tempo limite excedido ao buscar aluno."}
})
async def read_active_student_by_ra(ra: str, auth = Depends(authorization_api),db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
    """
    Retorna uma json com as informações de um aluno ativo pelo RA.
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
    
@router.get("/active/courses/{ra}", response_model=StudentWithCourses, summary="Busca um aluno ativo pelo RA com seus cursos", responses={
    200:{"description": "Detalhes do aluno com cursos retornados com sucesso."},
    400:{"description": "RA não pode ser vazio."},
    404:{"description": "Aluno não encontrado ou não está ativo."},
    500:{"description": "Erro interno ao buscar aluno."},
    504:{"description": "Tempo limite excedido ao buscar aluno."}
})
async def read_active_student_with_course(ra: str, auth = Depends(authorization_api), db: Session = Depends(get_db), get_api_key: str = Depends(get_api_key)):
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