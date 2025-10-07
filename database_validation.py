import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

encoded_password = quote_plus(MYSQL_PASSWORD or "")

# Formato de URL para MySQL com PyMySQL
# charset=utf8mb4 garante suporte a emojis e acentos
SQLALCHEMY_DATABASE_URL_MYSQL = (
    f"mysql+pymysql://{MYSQL_USERNAME}:{encoded_password}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
)

engine_mysql = create_engine(
    SQLALCHEMY_DATABASE_URL_MYSQL,
    pool_pre_ping=True,          # evita conexões “mortas”
    pool_recycle=1800,           # recicla conexões antigas (30 min)
    future=True
)

SessionLocalMySQL = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_mysql
)

BaseMySQL = declarative_base()

def get_db_mysql():
    db = SessionLocalMySQL()
    try:
        yield db
    finally:
        db.close()
