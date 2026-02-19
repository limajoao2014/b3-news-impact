import sys
import os
import json
import ollama

# Setup para importar módulos da pasta 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db import SessionLocal
from app.models import News

# NOME DO MODELO QUE VOCÊ BAIXOU (Se usou outro, troque aqui)
MODEL_NAME = "llama3.2:1b" 
# ou "mistral", "qwen2.5:1.5b", etc.

def analyze_news():
    db = SessionLocal()
    print(f"🧠 Iniciando Análise de IA com {MODEL_NAME}...")

    # 1. Busca notícias pendentes (onde sentimento é NULL)
    pending_news = db.query(News).filter(News.sentiment == None).all()
    
    if not pending_news:
        print("✅ Nenhuma notícia pendente para analisar.")
        return

    print(f"🔍 Encontrei {len(pending_news)} notícias para processar.")

    for news in pending_news:
        print(f"   🤖 Analisando ID {news.id}: {news.title[:50]}...")
        
        try:
            # 2. Monta o Prompt para a IA
            prompt = f"""
            Você é um analista financeiro sênior especializado em mercado brasileiro (B3).
            Analise a seguinte notícia e extraia:
            1. Sentimento (Positivo, Negativo ou Neutro).
            2. Score de Impacto (1 a 5, onde 5 é impacto extremo no preço da ação).
            
            Título: {news.title}
            Resumo: {news.summary}
            
            IMPORTANTE: Responda APENAS um JSON válido no seguinte formato, sem explicações adicionais:
            {{
                "sentiment": "Positivo",
                "score": 4
            }}
            """

            # 3. Chama o Ollama
            response = ollama.chat(model=MODEL_NAME, messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            content = response['message']['content']
            
            # Limpeza básica (caso a IA coloque ```json ... ```)
            clean_content = content.replace("```json", "").replace("```", "").strip()
            
            # 4. Converte o texto da IA para Dicionário Python
            result = json.loads(clean_content)
            
            # 5. Salva no Banco
            news.sentiment = result.get("sentiment", "Neutro")
            news.impact_score = result.get("score", 0)
            
            db.commit()
            print(f"      ✅ Resultado: {news.sentiment} (Impacto: {news.impact_score})")

        except json.JSONDecodeError:
            print(f"      ❌ Erro: A IA não retornou um JSON válido. Resposta crua: {content[:20]}...")
        except Exception as e:
            print(f"      ❌ Erro geral: {e}")
            db.rollback()

    print("🏁 Análise finalizada!")
    db.close()

if __name__ == "__main__":
    analyze_news()