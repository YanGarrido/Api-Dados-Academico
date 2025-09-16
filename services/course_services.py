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
        # --- Consulta 1: Buscar os dados do curso ---
        # Nota: A coluna CODCURSO é INT, então o parâmetro course_id deve ser int.
        query_curso = text("""
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
        
        course_data = db.execute(query_curso, {"course_id": course_id}).mappings().first()

        # Se o curso não for encontrado, retorna None imediatamente
        if not course_data:
            return None

        # --- Consulta 2: Buscar as disciplinas do curso ---
        query_disciplinas = text("""
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
        
        disciplinas_result = db.execute(query_disciplinas, {"course_id": course_id}).mappings().all()
        
        # O método .mappings().all() já retorna uma lista de dicionários no formato correto.
        # Apenas para manter o padrão idêntico ao seu outro service, criamos uma nova lista.
        subjects_list = [
            {"coddisc": item["coddisc"], "name": item["name"]}
            for item in disciplinas_result
        ]
        
        # --- 3. Combina os resultados ---
        # Converte o resultado do curso para um dicionário padrão
        response_data = dict(course_data)
        # Adiciona a lista de disciplinas
        response_data['subjects'] = subjects_list
        
        return response_data

    except Exception as e:
        print(f"Erro ao buscar curso com disciplinas: {e}")
        # Re-lança a exceção para que a camada superior (a rota) possa tratá-la
        raise e