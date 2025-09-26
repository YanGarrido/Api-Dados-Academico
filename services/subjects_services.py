from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.subject_schema import SubjectInfo, SubjectCompleteInfo

async def get_all_subjects(db: Session):
  try:
    sql_query = text("""
    SELECT 
      s.CODDISC AS disciplina_id, 
      s.NOME AS name, 
      s.CH AS ch, 
      s.CHESTAGIO AS chestagio, 
      s.CHTEORICA AS chteorica, 
      s.CHPRATICA AS chpratica, 
      s.CHEXTENSAO AS chextensao, 
      s.CHLABORATORIAL AS chlaboratorial  
    FROM CEMGJB_128187_RM_DV.dbo.SDISCIPLINA as s """)  
    
    results = db.execute(sql_query).mappings().all()
    return results
  
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    
    return []
  
async def get_complete_subjects(id: str, db: Session):
    try:
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
            (ISNUMERIC(:id) = 1 AND s.CODDISC = :id)
            OR
            (ISNUMERIC(:id) = 0 AND s.NOME = :id)""")
        
        params = {"id": id}
        
        subject_result_list = db.execute(sql_query_disciplina, params).mappings().all()

        if not subject_result_list:
            return None
        
        subject_data = subject_result_list[0]
        id_disciplina = subject_data['disciplina_id']

        query_courses = text("""
          SELECT DISTINCT 
            c.CODCURSO AS codcurso, 
            c.NOME AS name, 
            c.COMPLEMENTO AS complemento, 
            t.CODTURNO AS turno_id
          FROM CEMGJB_128187_RM_DV.dbo.SCURSO c
          JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL hf 
            ON c.CODCURSO = hf.CODCURSO 
          JOIN CEMGJB_128187_RM_DV.dbo.STURNO t 
            ON hf.CODTURNO = t.CODTURNO 
          JOIN CEMGJB_128187_RM_DV.dbo.SDISCGRADE dg 
            ON c.CODCURSO = dg.CODCURSO
          WHERE t.CODTURNO IN (1, 2, 3) AND dg.CODDISC = :id
        """)
        courses_results = db.execute(query_courses, {"id": id_disciplina}).mappings().all()
    
        response = {**subject_data, "cursos": courses_results}
        return response
        
    except Exception as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None
    
async def get_subjects_current_semester(codcurso: str, periodo_id: int, db: Session):
  print(periodo_id)
  try:
       sql_query = text("""
          SELECT DISTINCT
            s.CODDISC AS disciplina_id, 
            s.NOME AS name, 
            s.CH AS ch, 
            s.CHESTAGIO AS chestagio, 
            s.CHTEORICA AS chteorica,
            s.CHPRATICA AS chpratica, 
            s.CHEXTENSAO AS chextensao, 
            s.CHLABORATORIAL AS chlaboratorial
          FROM CEMGJB_128187_RM_DV.dbo.SDISCIPLINA s
          JOIN CEMGJB_128187_RM_DV.dbo.STURMADISC td 
            ON td.CODDISC = s.CODDISC
          JOIN CEMGJB_128187_RM_DV.dbo.STURMA t  
            ON t.CODTURMA = td.CODTURMA      
          JOIN CEMGJB_128187_RM_DV.dbo.STURNO tu 
            ON tu.CODFILIAL  = t.CODFILIAL        
          JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL hf 
            ON hf.IDHABILITACAOFILIAL = t.IDHABILITACAOFILIAL  
          WHERE td.IDPERLET = :periodo_id
            AND tu.CODTURNO IN (1,2,3)               
            AND hf.CODCURSO = :codcurso           
          ORDER BY s.NOME;""")  
       params = {"periodo_id": periodo_id, "codcurso": codcurso}
       rows = db.execute(sql_query, params).mappings().all()
       return rows
  
  except Exception as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None