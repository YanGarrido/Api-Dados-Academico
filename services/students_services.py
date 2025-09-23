from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.students_schema import StudentInfo

async def get_active_students(db: Session):
    """
    Executa a query SQL para buscar alunos ativos (com disciplinas).
    """
    try:
      sql_query = text("""
        SELECT DISTINCT
          ALUNO.RA AS ra,
          PESSOA.NOME AS name,
          PESSOA.EMAIL AS emailpessoal,
          SALUNOCOMPL.EMAIL AS email,
          PESSOA.TELEFONE1  AS telefone,
          PESSOA.CPF AS cpf
        FROM CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO 
        	ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI 
        	ON ALUNO.RA = MATRI.RA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS 
        	ON MATRI.CODSTATUS = STATUS.CODSTATUS
        JOIN CEMGJB_128187_RM_DV.dbo.SALUNOCOMPL
        	ON SALUNOCOMPL.RA = ALUNO.RA 
        WHERE
          STATUS.CODSTATUS IN (1, 9,16, 23)
      """)

      results = db.execute(sql_query).mappings().all()
      return results
    except Exception as e:
        print(f"Erro ao buscar alunos ativos: {e}")
        raise e

async def get_active_student_by_ra(ra: str, db: Session):
    try:
      sql_query = text("""
        SELECT DISTINCT
          ALUNO.RA AS ra,
          PESSOA.NOME AS name,
          PESSOA.EMAIL AS emailpessoal,
          SALUNOCOMPL.EMAIL AS email,
          PESSOA.TELEFONE1  AS telefone,
          PESSOA.CPF AS cpf
        FROM CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO 
        	ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI 
        	ON ALUNO.RA = MATRI.RA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS 
        	ON MATRI.CODSTATUS = STATUS.CODSTATUS
        JOIN CEMGJB_128187_RM_DV.dbo.SALUNOCOMPL
        	ON SALUNOCOMPL.RA = ALUNO.RA 
        WHERE
          STATUS.CODSTATUS IN (1, 9,16, 23) AND ALUNO.RA = :ra""")
      result = db.execute(sql_query, {"ra": ra}).mappings().first()
      return result
    except Exception as e:
        print(f"Erro ao buscar aluno ativo pelo RA: {e}")
        raise e

async def get_inactive_students(db: Session):
    try:
      sql_query = text("""
        SELECT DISTINCT
          ALUNO.RA AS ra,
          PESSOA.NOME AS name,
          PESSOA.EMAIL AS emailpessoal,
          SALUNOCOMPL.EMAIL AS email,
          PESSOA.TELEFONE1  AS telefone,
          PESSOA.CPF AS cpf
        FROM CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO 
        	ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI 
        	ON ALUNO.RA = MATRI.RA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS 
        	ON MATRI.CODSTATUS = STATUS.CODSTATUS
        JOIN CEMGJB_128187_RM_DV.dbo.SALUNOCOMPL
        	ON SALUNOCOMPL.RA = ALUNO.RA 
        WHERE
          STATUS.CODSTATUS NOT IN (1, 9,16, 23)""")
      
      results = db.execute(sql_query).mappings().all()
      return results
    except Exception as e:
        print(f"Erro ao buscar alunos inativos: {e}")
        raise e

#verificar se a logica de ex-alunos está correta com o professor
async def get_former_students(db: Session):
    try:
      sql_query = text("""
       SELECT DISTINCT
          ALUNO.RA AS ra,
          PESSOA.NOME AS name,
          PESSOA.EMAIL AS emailpessoal,
          SALUNOCOMPL.EMAIL AS email,
          PESSOA.TELEFONE1  AS telefone,
          PESSOA.CPF AS cpf
        FROM CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO 
        	ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI 
        	ON ALUNO.RA = MATRI.RA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS 
        	ON MATRI.CODSTATUS = STATUS.CODSTATUS
        JOIN CEMGJB_128187_RM_DV.dbo.SALUNOCOMPL
        	ON SALUNOCOMPL.RA = ALUNO.RA 
        WHERE
        STATUS.CODSTATUS IN (1, 9,16, 23) AND MATRI.IDPERLET = 55 
      """) # periodo atual 59 -- 2025/2
      results = db.execute(sql_query).mappings().all()
      return results
    except Exception as e:
        print(f"Erro ao buscar ex-alunos: {e}")
        raise e
    
async def get_active_student_with_course(ra: str, db: Session):
   try:
      query_student = text("""
      SELECT DISTINCT
          ALUNO.RA AS ra,
          PESSOA.NOME AS name,
          PESSOA.EMAIL AS emailpessoal,
          SALUNOCOMPL.EMAIL AS email,
          PESSOA.TELEFONE1  AS telefone,
          PESSOA.CPF AS cpf
        FROM CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO 
        	ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI 
        	ON ALUNO.RA = MATRI.RA
        INNER JOIN CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS 
        	ON MATRI.CODSTATUS = STATUS.CODSTATUS
        JOIN CEMGJB_128187_RM_DV.dbo.SALUNOCOMPL
        	ON SALUNOCOMPL.RA = ALUNO.RA 
        WHERE
          STATUS.CODSTATUS IN (1, 9,16, 23) AND ALUNO.RA = :ra""")
      
      student_data = db.execute(query_student, {"ra": ra}).mappings().first()

      if not student_data:
         return None
      
      query_courses = text("""
      SELECT DISTINCT 
        SCURSO.CODCURSO AS codcurso, 
        SCURSO.NOME AS name, 
        STURNO.CODTURNO AS turno_id  
      FROM CEMGJB_128187_RM_DV.dbo.SCURSO
      JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL
        ON SHABILITACAOFILIAL.CODCURSO = SCURSO.CODCURSO
      JOIN CEMGJB_128187_RM_DV.dbo.STURNO
        ON STURNO.CODTURNO = SHABILITACAOFILIAL.CODTURNO 
      JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOALUNO
        ON SHABILITACAOALUNO.IDHABILITACAOFILIAL = SHABILITACAOFILIAL.IDHABILITACAOFILIAL
      JOIN CEMGJB_128187_RM_DV.dbo.SALUNO
        ON SALUNO.RA = SHABILITACAOALUNO.RA 
      WHERE SALUNO.RA = :ra AND STURNO.CODTURNO IN (1,2,3)""")
      
      courses_result = db.execute(query_courses, {"ra": ra}).mappings().all()

      courses_list = [
         {"codcurso": item["codcurso"], "name": item["name"], "turno_id": item["turno_id"]}
         for item in courses_result
      ]

      response_data = dict(student_data)

      response_data["courses"] = courses_list

      return response_data
   
   except Exception as e:
      print(f"Erro ao buscar aluno com cursos matriculados: {e}")

      raise e

