import os
import dotenv
from fastapi import Depends, Header, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import text
from sqlalchemy.orm import Session
from database_validation import get_db_mysql

dotenv.load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False,description="Chave de Acesso da Aplicação.")
auth_header = "Authorization"
TABELA_APLICACOES = "carteiras.tblaplicacoes"

SERVER_API_KEY = os.getenv("SERVER_API_KEY")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="O cabeçalho X-API-Key está faltando"
        )
    
    if api_key_header == SERVER_API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="A Chave de API fornecida é inválida"
        )

async def authorization_api(db: Session = Depends(get_db_mysql),
                            auth_header: str | None = Header(default=None, alias=auth_header)
                            ):
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de acesso ausente."
        )
    sql = text(f"""
        SELECT intaplicacaoid
        FROM {TABELA_APLICACOES}
        WHERE strchave = :chave
          AND NOW() BETWEEN dtaativacao AND dtavalidade
    """)
    row = db.execute(sql, {"chave": auth_header}).first()

    if not row:
        raise HTTPException(
            status_code=403,
            detail="Chave de acesso inválida, expirada ou inativa."
        )

    # você pode retornar o id para auditoria/uso posterior
    return {"intaplicacaoid": row[0], "auth_header": auth_header}