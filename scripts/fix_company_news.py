import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.db import SessionLocal
from app.models import News, Company
from scripts.collect_news import COMPANY_ALIASES # Importa o dicionário que acabamos de criar

def fix_news():
    db = SessionLocal()
    print("🔧 Corrigindo vínculos de notícias antigas...")
    
    news_list = db.query(News).filter(News.company_id == None).all()
    companies = db.query(Company).all()

    # Recria o mapa (mesma lógica do coletor)
    keyword_map = {}
    for c in companies:
        c_name = c.name.lower()
        keyword_map[c_name] = c.id
        keyword_map[c.ticker.lower()] = c.id
        for alias in COMPANY_ALIASES.get(c_name, []):
            keyword_map[alias] = c.id

    count = 0
    for news in news_list:
        content = (news.title + " " + (news.summary or "")).lower()
        
        for keyword, c_id in keyword_map.items():
            if keyword in content: # Busca simples
                news.company_id = c_id
                count += 1
                print(f"   🔗 Conectado! '{news.title[:20]}...' -> ID {c_id}")
                break
    
    db.commit()
    print(f"✅ Correção concluída! {count} notícias foram vinculadas.")
    db.close()

if __name__ == "__main__":
    fix_news()