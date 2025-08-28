from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.professors_schema import ProfessorInfo

async def get_active_professors(db: Session):
    """
    Executa a query SQL para buscar professores ativos (com disciplinas).
    """
    try:
      sql_query = text("""
          SELECT DISTINCT
            GUS.CODUSUARIO AS code,
            PESSOA.NOME AS name, 
            PESSOA.EMAIL AS email
            
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
            AND TD.CODFILIAL = 2;
      """)

      # Executa a query e busca todos os resultados
      results = db.execute(sql_query).mappings().all()
      return results
    except Exception as e:
        print(f"Erro ao buscar professores ativos: {e}")
        raise e

async def get_professors_inactive(db: Session):
    try:
      sql_query = text("""
        SELECT
          GUS.CODUSUARIO AS code,
          PESSOA.NOME AS name,
          PESSOA.EMAIL AS email
      
        FROM
          CEMGJB_128187_RM_DV.dbo.SPROFESSOR AS PROF
          JOIN CEMGJB_128187_RM_DV.dbo.PPESSOA AS PESSOA
            ON PROF.CODPESSOA = PESSOA.CODIGO
          JOIN CEMGJB_128187_RM_DV.dbo.GUSUARIO AS GUS
            ON PESSOA.CODUSUARIO = GUS.CODUSUARIO
          LEFT JOIN CEMGJB_128187_RM_DV.dbo.SPROFESSORTURMA AS PT
            ON PROF.CODPROF = PT.CODPROF
          LEFT JOIN CEMGJB_128187_RM_DV.dbo.STURMADISC AS TD
            ON PT.IDTURMADISC = TD.IDTURMADISC
          LEFT JOIN CEMGJB_128187_RM_DV.dbo.SDISCIPLINA AS DISC
            ON TD.CODDISC = DISC.CODDISC
          LEFT JOIN CEMGJB_128187_RM_DV.dbo.SHABILITACAOFILIAL AS HF
            ON TD.IDHABILITACAOFILIAL = HF.IDHABILITACAOFILIAL
          LEFT JOIN CEMGJB_128187_RM_DV.dbo.SCURSO AS CUR
            ON HF.CODCURSO = CUR.CODCURSO
        WHERE
          PT.IDTURMADISC IS NULL
        ORDER BY
          PESSOA.NOME;""")
      results = db.execute(sql_query).mappings().all()
      return results
    except Exception as e:
        print(f"Erro ao buscar professores inativos: {e}")
        raise e
