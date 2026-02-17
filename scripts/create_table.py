from app.db import engine
from app.models import base

print("Criando tabelas...")
base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")