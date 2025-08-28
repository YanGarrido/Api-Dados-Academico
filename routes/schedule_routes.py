import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from security import get_api_key 
from schemas.schedule_schema import ScheduleInfo
from database import get_db
from services import schedule_services

router = APIRouter(
    prefix="/api/schedules",
    tags=["Schedules"]
)

@router.get("/", response_model=List[ScheduleInfo], status_code=status.HTTP_200_OK)
async def read_schedules(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)): 
    """
    Retorna uma lista de todos os horários.
    """
    try:
        schedules = await asyncio.wait_for(
            schedule_services.get_schedule(db),
            timeout=60.0
        )
        if not schedules:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Nenhum horário encontrado.")
        return schedules
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                            detail="Tempo limite excedido ao buscar horários.")
    except Exception as e:
        print(f"Erro ao buscar horários: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Erro interno ao buscar horários.")