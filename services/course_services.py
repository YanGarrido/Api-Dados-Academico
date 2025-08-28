from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.course_schema import CourseInfo
from schemas.subject_schema import SubjectInfo

async def get_all_courses(db: Session):
  try:
    sql_query = text("""
    SELECT DISTINCT SCURSO.CODCURSO AS id, SCURSO.NOME AS name, STURNO.CODTURNO AS turno_id
    FROM CEMGJB_128187_RM_DV.dbo.SCURSO 
    JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL 
    ON SCURSO.CODCURSO = SHABILITACAOFILIAL.CODCURSO 
    JOIN CEMGJB_128187_RM_DV.dbo.STURNO
    ON SHABILITACAOFILIAL.CODTURNO = STURNO.CODTURNO 
    WHERE STURNO.CODTURNO IN (1, 2, 3)
    """)
    results = db.execute(sql_query).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    return []

async def get_all_subjects(db: Session):
  try:
    sql_query = text("""
    SELECT s.CODDISC AS disciplina_id, s.NOME AS name, s.CH AS ch, s.CHESTAGIO AS chestagio, s.CHTEORICA AS chteorica, s.CHPRATICA AS chpratica, s.CHEXTENSAO AS chextensao, s.CHLABORATORIAL AS chlaboratorial  FROM CEMGJB_128187_RM_DV.dbo.SDISCIPLINA as s
    """)  
    results = db.execute(sql_query).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    return []