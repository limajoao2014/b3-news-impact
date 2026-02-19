import os
from dotenv import load_dotenv  # Importa a função que lê o .env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. FORÇA O CARREGAMENTO DO .ENV
load_dotenv()

# 2. TENTA PEGAR A URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. DEBUG (Isso vai imprimir no terminal para te mostrar o que está acontecendo)
print(f"DEBUG: Tentando conectar em: {DATABASE_URL}")

# 4. TRAVA DE SEGURANÇA (Para o erro ser mais claro se falhar)
if not DATABASE_URL:
    raise ValueError("ERRO FATAL: A variável DATABASE_URL não foi encontrada. Verifique se o arquivo .env existe e não está vazio.")

# Cria a conexão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()