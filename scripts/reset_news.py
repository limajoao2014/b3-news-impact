import sys
import os
from sqlalchemy import text

# Setup para importar módulos da pasta 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db import engine

def force_drop_news():
    print("💣 Iniciando operação de limpeza da tabela News...")
    
    with engine.connect() as connection:
        # O comando CASCADE garante que ela seja apagada mesmo se tiver vínculos
        try:
            connection.execute(text("DROP TABLE IF EXISTS news CASCADE;"))
            connection.commit()
            print("✅ Tabela 'news' foi deletada com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao tentar deletar: {e}")

if __name__ == "__main__":
    force_drop_news()