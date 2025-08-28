import os
import dotenv
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

dotenv.load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
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