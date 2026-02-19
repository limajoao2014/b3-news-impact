import sys
import os
import feedparser
from datetime import datetime
from time import mktime
from sqlalchemy import or_

# Setup para importar módulos da pasta 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db import SessionLocal
from app.models import Company, News

# Lista de Feeds
RSS_FEEDS = {
    "InfoMoney": "https://www.infomoney.com.br/feed/",
    "Brazil Journal": "https://braziljournal.com/feed/",
    "Investing Brasil": "https://br.investing.com/rss/news_25.rss",
    "Valor Econômico": "https://www.valor.com.br/rss"
}

# AJUDA O ROBÔ A ENCONTRAR AS EMPRESAS
# (Adicione aqui apelidos comuns para melhorar a busca)
COMPANY_ALIASES = {
    "petrobras": ["petrobras", "petr4", "petr3", "estatal"],
    "vale": ["vale", "vale3", "mineradora"],
    "itaú unibanco": ["itaú", "itau", "itub4", "itub3"],
    "banco do brasil": ["banco do brasil", "bbas3", "bb"],
    "weg": ["weg", "wege3"],
    "magazine luiza": ["magalu", "magazine luiza", "mglu3"],
    "b3": ["b3", "b3sa3", "bolsa"],
    "prio": ["prio", "petrorio", "prio3"],
    "bradesco": ["bradesco", "bbdc4", "bbdc3"],
    "ambev": ["ambev", "abev3"]
}

def collect_news():
    db = SessionLocal()
    print("📰 Iniciando coleta INTELIGENTE de notícias...")

    # Carrega empresas do banco
    companies = db.query(Company).all()
    
    # Cria um mapa reverso: Termo de Busca -> ID da Empresa
    # Ex: 'magalu' -> ID 5, 'mglu3' -> ID 5
    keyword_map = {}
    
    for company in companies:
        # Usa o nome oficial (em minúsculo)
        c_name = company.name.lower()
        keyword_map[c_name] = company.id
        keyword_map[company.ticker.lower()] = company.id
        
        # Adiciona os apelidos manuais se existirem
        aliases = COMPANY_ALIASES.get(c_name, [])
        for alias in aliases:
            keyword_map[alias] = company.id

    try:
        new_count = 0
        for source, url in RSS_FEEDS.items():
            print(f"   📡 Lendo: {source}...")
            feed = feedparser.parse(url)

            for entry in feed.entries:
                # 1. Verifica duplicidade
                exists = db.query(News).filter(News.url == entry.link).first()
                if exists:
                    continue

                # 2. Converte data
                pub_date = datetime.now()
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime.fromtimestamp(mktime(entry.published_parsed))

                # 3. Tenta encontrar a empresa (MATCH)
                company_id = None
                
                # Procura no Título E no Resumo para aumentar as chances
                content_to_search = (entry.title + " " + entry.get('summary', '')).lower()
                
                # Verifica cada palavra chave
                for keyword, c_id in keyword_map.items():
                    # Usa verificação de palavra inteira (básica) para evitar falsos positivos
                    # Ex: evitar que "vale" dê match em "equivalente"
                    if f" {keyword} " in f" {content_to_search} " or \
                       content_to_search.startswith(keyword + " ") or \
                       content_to_search.endswith(" " + keyword):
                        company_id = c_id
                        break # Achou uma, para (assume a primeira encontrada)

                # 4. Salva (mesmo sem empresa, para registro geral)
                new_news = News(
                    company_id=company_id,
                    title=entry.title,
                    summary=entry.summary if 'summary' in entry else entry.title,
                    url=entry.link,
                    source=source,
                    published_at=pub_date
                )
                db.add(new_news)
                new_count += 1
                
                # Feedback visual
                match_status = f"✅ Vinculado a ID {company_id}" if company_id else "⚠️ Geral (Sem vínculo)"
                # print(f"      ➕ {match_status}: {entry.title[:30]}...")

        db.commit()
        print(f"🏁 Coleta finalizada! {new_count} novas notícias adicionadas.")

    except Exception as e:
        print(f"❌ Erro na coleta: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    collect_news()