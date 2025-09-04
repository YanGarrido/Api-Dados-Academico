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

async def get_professors_with_subjects(codigo_professor: str, db: Session):
    """
    Busca os detalhes de um professor e aninha uma lista com os nomes de suas disciplinas.
    """
    try:
        # --- Consulta 1: Buscar os dados do professor ---
        query_professor = text("""
            SELECT
                GUS.CODUSUARIO AS code,
                PESSOA.NOME AS name,
                PESSOA.CPF AS cpf,
                PESSOA.EMAILPESSOAL AS emailpessoal,
                PESSOA.EMAIL AS email
            FROM
                CEMGJB_128187_RM_DV.dbo.GUSUARIO AS GUS
                JOIN CEMGJB_128187_RM_DV.dbo.PPESSOA AS PESSOA ON GUS.CODUSUARIO = PESSOA.CODUSUARIO
            WHERE
                GUS.CODUSUARIO = :codigo_prof
        """)
        
        professor_data = db.execute(query_professor, {"codigo_prof": codigo_professor}).mappings().first()

        # Se o professor não for encontrado, retorna None imediatamente
        if not professor_data:
            return None

        # --- Consulta 2: Buscar os nomes das disciplinas do professor ---
        query_disciplinas = text("""
            SELECT
                DISC.NOME
            FROM
                CEMGJB_128187_RM_DV.dbo.SPROFESSOR AS PROF
                JOIN CEMGJB_128187_RM_DV.dbo.SPROFESSORTURMA AS PT ON PROF.CODPROF = PT.CODPROF
                JOIN CEMGJB_128187_RM_DV.dbo.STURMADISC AS TD ON PT.IDTURMADISC = TD.IDTURMADISC
                JOIN CEMGJB_128187_RM_DV.dbo.SDISCIPLINA AS DISC ON TD.CODDISC = DISC.CODDISC
                JOIN CEMGJB_128187_RM_DV.dbo.PPESSOA AS PESSOA ON PROF.CODPESSOA = PESSOA.CODIGO
                JOIN CEMGJB_128187_RM_DV.dbo.GUSUARIO AS GUS ON PESSOA.CODUSUARIO = GUS.CODUSUARIO
            WHERE
                GUS.CODUSUARIO = :codigo_prof
            ORDER BY
                DISC.NOME
        """)
        
        disciplinas_result = db.execute(query_disciplinas, {"codigo_prof": codigo_professor}).mappings().all()
        
        # Extrai apenas os nomes das disciplinas para uma lista de strings
        lista_de_nomes_disciplinas = [item['NOME'] for item in disciplinas_result]
        
        # --- 3. Combina os resultados ---
        # Converte o resultado do professor para um dicionário padrão
        response_data = dict(professor_data)
        # Adiciona a lista de disciplinas
        response_data['subjects'] = lista_de_nomes_disciplinas
        
        return response_data

    except Exception as e:
        print(f"Erro ao buscar professor com disciplinas: {e}")
        raise e