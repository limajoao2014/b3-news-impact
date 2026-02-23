from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa o arquivo de rotas de notícias que você acabou de criar
from app.api.news import router as news_router
from app.api.prices import router as prices_router


app = FastAPI(
    title="B3 News Impact API",
    description="API para analisar o impacto de notícias nas ações da B3",
    version="1.0.0"
)

# Configuração de CORS (Essencial para que o seu futuro Dashboard consiga ler esses dados)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite acesso de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# "Pluga" a rota de notícias no servidor principal
app.include_router(news_router, prefix="/api/news", tags=["Notícias"])
app.include_router(prices_router, prefix="/api/prices", tags=["Preços"])
# Rota raiz (só para testar se o servidor tá vivo)
@app.get("/")
def read_root():
    return {"status": "🚀 API B3 News Impact rodando com sucesso!"}