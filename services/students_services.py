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
          PESSOA.EMAIL AS email
        FROM
          CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI ON ALUNO.RA = MATRI.RA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS ON MATRI.CODSTATUS = STATUS.CODSTATUS
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
          PESSOA.EMAIL AS email
        FROM
          CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI ON ALUNO.RA = MATRI.RA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS ON MATRI.CODSTATUS = STATUS.CODSTATUS
        WHERE
          STATUS.CODSTATUS IN (1, 9,16, 23) AND ALUNO.RA = :ra
      """)
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
          PESSOA.EMAIL AS email
        FROM
          CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI ON ALUNO.RA = MATRI.RA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS ON MATRI.CODSTATUS = STATUS.CODSTATUS
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
          PESSOA.EMAIL AS email
        FROM
          CEMGJB_128187_RM_DV.dbo.PPESSOA  AS PESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SALUNO AS ALUNO ON PESSOA.CODIGO = ALUNO.CODPESSOA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SMATRICPL AS MATRI ON ALUNO.RA = MATRI.RA
        INNER JOIN
          CEMGJB_128187_RM_DV.dbo.SSTATUS AS STATUS ON MATRI.CODSTATUS = STATUS.CODSTATUS
        WHERE
        STATUS.CODSTATUS IN (1, 9,16, 23) AND MATRI.IDPERLET = 55 
      """) # periodo atual 59 -- 2025/2
      results = db.execute(sql_query).mappings().all()
      return results
    except Exception as e:
        print(f"Erro ao buscar ex-alunos: {e}")
        raise e