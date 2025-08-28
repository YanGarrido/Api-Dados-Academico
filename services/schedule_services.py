from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.schedule_schema import ScheduleInfo

async def get_schedule(db: Session):
  """
  Executa a query SQL para buscar informações de horários.
  """
  try:
    sql_query = text("""
    SELECT DISTINCT
      s.CODTURNO AS codturno , 
      s.HORAINICIAL AS horainicial, 
      s.HORAFINAL AS horafinal  
    FROM CEMGJB_128187_RM_DV.dbo.SHORARIO s """)

    # Executa a query e busca todos os resultados
    results = db.execute(sql_query).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao buscar horários: {e}")
    raise e