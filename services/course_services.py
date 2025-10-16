from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.course_schema import CourseInfo, CourseWithSubjects, BaseSubject

async def get_all_courses(db: Session):
  try:
    sql_query = text("""
    SELECT DISTINCT 
      SCURSO.CODCURSO AS codcurso, 
      SCURSO.NOME AS nome, 
      SCURSO.COMPLEMENTO AS complemento, 
      STURNO.CODTURNO AS codturno
    FROM CEMGJB_128187_RM_DV.dbo.SCURSO 
    JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL 
      ON SCURSO.CODCURSO = SHABILITACAOFILIAL.CODCURSO 
    JOIN CEMGJB_128187_RM_DV.dbo.STURNO
      ON SHABILITACAOFILIAL.CODTURNO = STURNO.CODTURNO 
    WHERE STURNO.CODTURNO IN (1, 2, 3)
      AND SCURSO.CODCURSO IN ('1','2', '4', '5', '6','10','22')
    """)
    results = db.execute(sql_query).mappings().all()
    return results
  except Exception as e:
    print(f"Erro ao executar a consulta SQL: {e}")
    return []
  
async def get_course_with_subjects(codcurso: int, db: Session):
    """
    Busca os detalhes de um curso e aninha uma lista com suas disciplinas.
    O padrão deste código imita o da função get_professors_with_subjects.
    """
    try:
        query_course = text("""
            SELECT TOP 1
                SCURSO.CODCURSO AS codcurso, 
                SCURSO.NOME AS nome, 
                SCURSO.COMPLEMENTO AS complemento, 
                SHABILITACAOFILIAL.CODTURNO AS codturno
            FROM 
                SCURSO 
            JOIN 
                SHABILITACAOFILIAL ON SCURSO.CODCURSO = SHABILITACAOFILIAL.CODCURSO 
            WHERE 
                SCURSO.CODCURSO = :codcurso
        """)

        course_data = db.execute(query_course, {"codcurso": codcurso}).mappings().first()

        if not course_data:
            return None

        # --- Consulta 2: Buscar as disciplinas do curso ---
        query_subjects = text("""
            SELECT DISTINCT
                D.CODDISC AS coddisc,
                D.NOME    AS nome
            FROM SDISCIPLINA AS D
            JOIN STURMADISC  AS TD ON TD.CODDISC = D.CODDISC
            JOIN SHABILITACAOFILIAL AS H ON H.IDHABILITACAOFILIAL  = TD.IDHABILITACAOFILIAL 
            JOIN SCURSO      AS C  ON C.CODCURSO = H.CODCURSO
            JOIN STURNO      AS T ON T.CODTURNO = H.CODTURNO
            WHERE C.CODCURSO = :codcurso AND T.CODTURNO IN (1, 2, 3)
            ORDER BY D.NOME
        """)

        subjects_result = db.execute(query_subjects, {"codcurso": codcurso}).mappings().all()

    
        subjects_list = [
            {"coddisc": item["coddisc"], "nome": item["nome"]}
            for item in subjects_result
        ]
        
       
        response_data = dict(course_data)
        
        response_data['subjects'] = subjects_list
        
        return response_data

    except Exception as e:
        print(f"Erro ao buscar curso com disciplinas: {e}")
       
        raise e
    
async def has_class_period(codcurso: str,periodo_letivo_id: int, periodo: int, codturno: int, db: Session):
   try:
      sql_query=text("""
        WITH alvo AS (
            SELECT DISTINCT M.RA
        FROM CEMGJB_128187_RM_DV.dbo.SMATRICPL AS M
        JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL AS HF
          ON HF.IDHABILITACAOFILIAL = M.IDHABILITACAOFILIAL 
        WHERE HF.CODCURSO = :codcurso
          AND M.IDPERLET = :periodo_letivo_id
          AND M.PERIODO = :periodo
          AND HF.CODTURNO = :codturno  
          AND M.CODSTATUS IN (1,9,16,23)
        )
        SELECT
        CAST(CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END AS BIT) AS tem_turma,
        COUNT(*) AS quant_alunos
        FROM alvo; """)
      result = db.execute(sql_query, {"codcurso": codcurso, "periodo_letivo_id": periodo_letivo_id, "periodo": periodo,"codturno":codturno}).mappings().first() or {"tem_turma": False, "quant_alunos": 0}
      
      return {"tem_turma": bool(result["tem_turma"]), "quant_alunos": int(result["quant_alunos"])}
   except Exception as e:
       print(f"Erro ao buscar se possuir turma: {e}")

       raise e
      
      # todas as turmas nesses semestre ativas
async def semester_class_active(periodo_letivo_id: int, periodo: int, codturno: int, db: Session):
   try:
      sql_query=text("""
      SELECT
        c.CODCURSO AS codcurso,
        c.NOME AS nome,
        c.COMPLEMENTO AS complemento,
        tu.NOME AS turno_nome,
        m.PERIODO AS periodo,
        COUNT(DISTINCT m.RA) AS quant_alunos
      FROM CEMGJB_128187_RM_DV.dbo.SCURSO c
      JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL hf 
        ON hf.CODCURSO = c.CODCURSO
      JOIN CEMGJB_128187_RM_DV.dbo.SMATRICPL m  
        ON m.IDHABILITACAOFILIAL = hf.IDHABILITACAOFILIAL
      LEFT JOIN CEMGJB_128187_RM_DV.dbo.STURNO tu 
        ON tu.CODTURNO = hf.CODTURNO
      WHERE m.IDPERLET   = :periodo_letivo_id
          AND m.CODSTATUS IN (1,9,16,23)             
          AND m.PERIODO   IN (:periodo)             
          AND hf.CODTURNO = :codturno
      GROUP BY c.CODCURSO, c.NOME, c.COMPLEMENTO, tu.NOME, m.PERIODO
      ORDER BY c.NOME, m.PERIODO;""")
      
      result = db.execute(sql_query, {"periodo_letivo_id":periodo_letivo_id, "periodo":periodo, "codturno":codturno}).mappings().all()
      
      return result
   except Exception as e:
       print(f"Erro ao buscar as turmas ativas nesse semestre: {e}")

       raise e
      
async def get_course_with_professors(codcurso: str, db: Session):
    """
    Busca os detalhes de um curso e aninha uma lista com suas disciplinas.
    O padrão deste código imita o da função get_professors_with_subjects.
    """
    try:
        query_course = text("""
            SELECT TOP 1
                SCURSO.CODCURSO AS codcurso, 
                SCURSO.NOME AS nome, 
                SCURSO.COMPLEMENTO AS complemento, 
                SHABILITACAOFILIAL.CODTURNO AS codturno
            FROM 
                SCURSO 
            JOIN 
                SHABILITACAOFILIAL ON SCURSO.CODCURSO = SHABILITACAOFILIAL.CODCURSO 
            WHERE 
                SCURSO.CODCURSO = :codcurso
        """)

        course_data = db.execute(query_course, {"codcurso": codcurso}).mappings().first()

        if not course_data:
            return None

        # --- Consulta 2: Buscar os professores do curso ---
        query_professors = text("""
          SELECT DISTINCT
            GUS.CODUSUARIO AS code,
            PESSOA.NOME AS nome, 
            PESSOA.EMAILPESSOAL AS emailpessoal,
            PESSOA.EMAIL AS email,
            PESSOA.CPF AS cpf
            
          FROM
            CEMGJB_128187_RM_DV.dbo.SPROFESSORTURMA AS PT
            JOIN CEMGJB_128187_RM_DV.dbo.SPROFESSOR AS PROF
              ON PT.CODCOLIGADA = PROF.CODCOLIGADA
              AND PT.CODPROF = PROF.CODPROF
            JOIN CEMGJB_128187_RM_DV.dbo.PPESSOA AS PESSOA
            ON PROF.CODPESSOA  = PESSOA.CODIGO
            JOIN CEMGJB_128187_RM_DV.dbo.GUSUARIO AS GUS
              ON PESSOA.CODUSUARIO = GUS.CODUSUARIO 
            JOIN CEMGJB_128187_RM_DV.dbo.STURMADISC AS TD
              ON PT.IDTURMADISC = TD.IDTURMADISC
            JOIN CEMGJB_128187_RM_DV.dbo.SDISCIPLINA AS DISC
              ON TD.CODDISC = DISC.CODDISC
            LEFT JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL AS HF
              ON TD.IDHABILITACAOFILIAL = HF.IDHABILITACAOFILIAL
            LEFT JOIN CEMGJB_128187_RM_DV.dbo.SCURSO AS CUR
              ON HF.CODCURSO = CUR.CODCURSO
          WHERE
            TD.CODTIPOCURSO = 1
            AND TD.CODFILIAL = 2
            AND CUR.CODCURSO = :codcurso;
      """)
        professors_result = db.execute(query_professors, {"codcurso": codcurso}).mappings().all()

        professors_list = [
            {"code": item["code"], "nome": item["nome"], "emailpessoal": item["emailpessoal"], "email": item["email"], "cpf": item["cpf"]}
            for item in professors_result
        ]
        
       
        response_data = dict(course_data)

        response_data['professors'] = professors_list

        return response_data

    except Exception as e:
        print(f"Erro ao buscar curso com disciplinas: {e}")
       
        raise e