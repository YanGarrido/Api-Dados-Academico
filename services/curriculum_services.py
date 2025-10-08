from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.curriculum_schema import CurriculumInfo


async def get_curriculum(db:Session):
  """
  Executa a query SQL para buscar o currículo de um curso específico.
  """
  try:
    sql_query = text("""
    SELECT 
    s.CODPERIODO AS periodo, 
    s.CODCURSO AS curso_id, 
    s.CODDISC AS disciplina_id,
    s.CODGRADE AS codgrade,
    s.DESCRICAO AS descricao  
    FROM CEMGJB_128187_RM_DV.dbo.SDISCGRADE s 
    WHERE s.CODGRADE ='20231' AND s.CODPERIODO != 0 AND s.CODCURSO IN ('1','2','4','5','6','10','22')
    """)
    results = db.execute(sql_query).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    raise e

async def get_curriculum_current_course(codcurso: str,db:Session):
  """
  Executa a query SQL para buscar o currículo de um curso específico.
  """
  try:
    sql_query = text("""
    SELECT 
    s.CODPERIODO AS periodo, 
    s.CODCURSO AS curso_id, 
    s.CODDISC AS disciplina_id,  
    s.CODGRADE AS codgrade,
    s.DESCRICAO AS descricao
    FROM CEMGJB_128187_RM_DV.dbo.SDISCGRADE s 
    WHERE s.CODCURSO = :codcurso AND s.CODGRADE ='20231' AND s.CODPERIODO != 0
    """)
    results = db.execute(sql_query, {"codcurso": codcurso}).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    raise e
  
async def get_old_curriculum(codcurso: str, db:Session):
  """
  Executa a query SQL para buscar o currículo dos cursos.
  """
  try:
    sql_query = text("""
    SELECT 
    s.CODPERIODO AS periodo, 
    s.CODCURSO AS curso_id, 
    s.CODDISC AS disciplina_id,  
    s.CODGRADE AS codgrade,
    s.DESCRICAO AS descricao 
    FROM CEMGJB_128187_RM_DV.dbo.SDISCGRADE s 
    WHERE s.CODCURSO = :codcurso AND s.CODGRADE ='20172' AND s.CODPERIODO != 0
    """)
    results = db.execute(sql_query, {"codcurso": codcurso}).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    raise e