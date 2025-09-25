from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.course_schema import CourseInfo, CourseWithSubjects, BaseSubject

async def get_all_courses(db: Session):
  try:
    sql_query = text("""
    SELECT DISTINCT 
      SCURSO.CODCURSO AS codcurso, 
      SCURSO.NOME AS name, 
      SCURSO.COMPLEMENTO AS complemento, 
      STURNO.CODTURNO AS turno_id
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
  
async def get_course_with_subjects(course_id: int, db: Session):
    """
    Busca os detalhes de um curso e aninha uma lista com suas disciplinas.
    O padrão deste código imita o da função get_professors_with_subjects.
    """
    try:
        query_course = text("""
            SELECT TOP 1
                SCURSO.CODCURSO AS codcurso, 
                SCURSO.NOME AS name, 
                SCURSO.COMPLEMENTO AS complemento, 
                SHABILITACAOFILIAL.CODTURNO AS turno_id
            FROM 
                SCURSO 
            JOIN 
                SHABILITACAOFILIAL ON SCURSO.CODCURSO = SHABILITACAOFILIAL.CODCURSO 
            WHERE 
                SCURSO.CODCURSO = :course_id
        """)
        
        course_data = db.execute(query_course, {"course_id": course_id}).mappings().first()

        if not course_data:
            return None

        # --- Consulta 2: Buscar as disciplinas do curso ---
        query_subjects = text("""
            SELECT DISTINCT
                D.CODDISC AS coddisc,
                D.NOME    AS name
            FROM SDISCIPLINA AS D
            JOIN STURMADISC  AS TD ON TD.CODDISC = D.CODDISC
            JOIN SHABILITACAOFILIAL AS H ON H.IDHABILITACAOFILIAL  = TD.IDHABILITACAOFILIAL 
            JOIN SCURSO      AS C  ON C.CODCURSO = H.CODCURSO
            JOIN STURNO      AS T ON T.CODTURNO = H.CODTURNO
            WHERE C.CODCURSO = :course_id AND T.CODTURNO IN (1, 2, 3)
            ORDER BY D.NOME
        """)
        
        subjects_result = db.execute(query_subjects, {"course_id": course_id}).mappings().all()
        
    
        subjects_list = [
            {"coddisc": item["coddisc"], "name": item["name"]}
            for item in subjects_result
        ]
        
       
        response_data = dict(course_data)
        
        response_data['subjects'] = subjects_list
        
        return response_data

    except Exception as e:
        print(f"Erro ao buscar curso com disciplinas: {e}")
       
        raise e
    
async def has_class_first_period(codcurso: str,periodoletivo_id: int, periodo_id: int, codturno: int, db: Session):
   try:
      sql_query=text("""
        WITH alvo AS (
            SELECT DISTINCT M.RA
        FROM CEMGJB_128187_RM_DV.dbo.SMATRICPL AS M
        JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL AS HF
          ON HF.IDHABILITACAOFILIAL = M.IDHABILITACAOFILIAL 
        WHERE HF.CODCURSO = :codcurso
          AND M.IDPERLET = :periodoletivo_id
          AND M.PERIODO = :periodo_id  
          AND HF.CODTURNO = :codturno  
          AND M.CODSTATUS IN (1,9,16,23)
        )
        SELECT
        CAST(CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END AS BIT) AS tem_turma,
        COUNT(*) AS quant_alunos
        FROM alvo; """)
      result = db.execute(sql_query, {"codcurso": codcurso, "periodoletivo_id": periodoletivo_id, "periodo_id": periodo_id,"codturno":codturno}).mappings().first() or {"tem_turma": False, "quant_alunos": 0}
      
      return {"tem_turma": bool(result["tem_turma"]), "quant_alunos": int(result["quant_alunos"])}
   except Exception as e:
       print(f"Erro ao buscar se possuir turma: {e}")

       raise e
      
      # turmas nesses semestre ativas