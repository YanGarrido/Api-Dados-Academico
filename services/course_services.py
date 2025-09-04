from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.course_schema import CourseInfo
from schemas.subject_schema import SubjectInfo

async def get_all_courses(db: Session):
  try:
    sql_query = text("""
    SELECT DISTINCT SCURSO.CODCURSO AS id, SCURSO.NOME AS name, SCURSO.COMPLEMENTO AS complemento, STURNO.CODTURNO AS turno_id
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
  
# Em seu arquivo de serviço (ex: services/course_services.py)

async def get_complete_subjects(id: str, db: Session):
    try:
        # A query agora compara string com string para o CODDISC
        sql_query_disciplina = text("""
            SELECT 
                s.CODDISC AS disciplina_id, 
                s.NOME AS name, 
                s.CH AS ch, 
                s.CHESTAGIO AS chestagio, 
                s.CHTEORICA AS chteorica, 
                s.CHPRATICA AS chpratica, 
                s.CHEXTENSAO AS chextensao, 
                s.CHLABORATORIAL AS chlaboratorial  
            FROM CEMGJB_128187_RM_DV.dbo.SDISCIPLINA as s
            WHERE 
                -- Se o parâmetro parece um número, compara com CODDISC (como string)
                (ISNUMERIC(:id_param) = 1 AND s.CODDISC = :id_param) -- <-- MUDANÇA AQUI
                OR
                -- Se não parece um número, compara com NOME
                (ISNUMERIC(:id_param) = 0 AND s.NOME = :id_param)
        """)
        
        params = {"id_param": id}
        
        subject_result_list = db.execute(sql_query_disciplina, params).mappings().all()

        if not subject_result_list:
            return None
        
        subject_data = subject_result_list[0]
        id_disciplina = subject_data['disciplina_id']

        # A segunda consulta para buscar os cursos não precisa de alteração,
        # pois id_disciplina já será a string correta (ex: '0001')
        query_courses = text("""
            SELECT 
                DISTINCT c.CODCURSO AS id, c.NOME AS name, 
                c.COMPLEMENTO AS complemento, t.CODTURNO AS turno_id
            FROM CEMGJB_128187_RM_DV.dbo.SCURSO c
            JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL hf ON c.CODCURSO = hf.CODCURSO 
            JOIN CEMGJB_128187_RM_DV.dbo.STURNO t ON hf.CODTURNO = t.CODTURNO 
            JOIN CEMGJB_128187_RM_DV.dbo.SDISCGRADE dg ON c.CODCURSO = dg.CODCURSO
            WHERE t.CODTURNO IN (1, 2, 3) AND dg.CODDISC = :id
        """)
        courses_results = db.execute(query_courses, {"id": id_disciplina}).mappings().all()
    
        response = {**subject_data, "cursos": courses_results}
        return response
        
    except Exception as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None