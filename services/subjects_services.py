from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.subject_schema import SubjectInfo, SubjectCompleteInfo
from typing import List

async def get_all_subjects(db: Session):
  try:
    sql_query = text("""
    SELECT 
      s.CODDISC AS coddisc, 
      s.NOME AS nome, 
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
  
async def get_complete_subjects(coddisc: str, db: Session):
    try:
        sql_query_disciplina = text("""
          SELECT 
            s.CODDISC AS coddisc, 
            s.NOME AS nome, 
            s.CH AS ch, 
            s.CHESTAGIO AS chestagio, 
            s.CHTEORICA AS chteorica, 
            s.CHPRATICA AS chpratica, 
            s.CHEXTENSAO AS chextensao, 
            s.CHLABORATORIAL AS chlaboratorial
          FROM CEMGJB_128187_RM_DV.dbo.SDISCIPLINA as s
          WHERE     
            (ISNUMERIC(:coddisc) = 1 AND s.CODDISC = :coddisc)
            OR
            (ISNUMERIC(:coddisc) = 0 AND s.NOME = :coddisc)""")

        params = {"coddisc": coddisc}

        subject_result_list = db.execute(sql_query_disciplina, params).mappings().all()

        if not subject_result_list:
            return None
        
        subject_data = subject_result_list[0]
        coddisc = subject_data['coddisc']

        query_courses = text("""
          SELECT DISTINCT 
            c.CODCURSO AS codcurso, 
            c.NOME AS nome, 
            c.COMPLEMENTO AS complemento, 
            t.CODTURNO AS codturno
          FROM CEMGJB_128187_RM_DV.dbo.SCURSO c
          JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL hf 
            ON c.CODCURSO = hf.CODCURSO 
          JOIN CEMGJB_128187_RM_DV.dbo.STURNO t 
            ON hf.CODTURNO = t.CODTURNO 
          JOIN CEMGJB_128187_RM_DV.dbo.SDISCGRADE dg 
            ON c.CODCURSO = dg.CODCURSO
          WHERE t.CODTURNO IN (1, 2, 3) AND dg.CODDISC = :coddisc
        """)
        courses_results = db.execute(query_courses, {"coddisc": coddisc}).mappings().all()
    
        response = {**subject_data, "cursos": courses_results}
        return response
        
    except Exception as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None

async def get_subjects_current_semester(codcursos: List[str], periodo_letivo_id: int, db: Session):
    print(f"Período: {periodo_letivo_id}, Cursos: {codcursos}")
    try:
        # Criar placeholders dinâmicos para múltiplos cursos
        placeholders = ",".join([f":codcurso_{i}" for i in range(len(codcursos))])
        
        sql_query = text(f"""
            SELECT DISTINCT
                s.CODDISC AS coddisc, 
                s.NOME AS nome, 
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
                ON tu.CODFILIAL = t.CODFILIAL        
            JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL hf 
                ON hf.IDHABILITACAOFILIAL = t.IDHABILITACAOFILIAL  
            WHERE td.IDPERLET = :periodo_letivo_id
                AND tu.CODTURNO IN (1,2,3)               
                AND hf.CODCURSO IN ({placeholders})           
            ORDER BY s.NOME
        """)
        
        # Criar parâmetros dinâmicos
        params = {"periodo_letivo_id": periodo_letivo_id}
        for i, curso in enumerate(codcursos):
            params[f"codcurso_{i}"] = curso
        
        print(f"Query executada: {sql_query}")
        print(f"Parâmetros: {params}")
        
        rows = db.execute(sql_query, params).mappings().all()
        print(f"Encontradas {len(rows)} disciplinas")
        return rows
    
    except Exception as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return None