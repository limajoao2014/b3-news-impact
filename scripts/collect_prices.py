print("1. O script collect_prices começou a rodar!") # <--- TESTE 1

import sys
import os
import yfinance as yf
from datetime import datetime

# Ajusta o caminho para encontrar a pasta 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print("2. Importando banco de dados...") # <--- TESTE 2
from app.db import SessionLocal
from app.models import Company, Price

def update_prices():
    print("3. Dentro da função update_prices!") # <--- TESTE 3
    db = SessionLocal()
    
    try:
        companies = db.query(Company).all()
        print(f"4. Encontrei {len(companies)} empresas no banco.") # <--- TESTE 4

        for company in companies:
            ticker_yf = f"{company.ticker}.SA"
            print(f"   -> Buscando preço para: {ticker_yf}...")
            
            # Tenta pegar o preço
            stock = yf.Ticker(ticker_yf)
            
            # Truque para pegar o preço mais rápido (fast_info)
            # Às vezes o .history() falha ou demora
            try:
                price = stock.fast_info['last_price']
            except:
                # Fallback se o fast_infso falhar
                hist = stock.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                else:
                    price = None

            if price:
                print(f"      Preço encontrado: R$ {price:.2f}")
                new_price = Price(
                    company_id=company.id,
                    price=float(price),
                    date=datetime.now()
                )
                db.add(new_price)
            else:
                print("      ❌ Não conseguiu pegar o preço.")

        db.commit()
        print("5. Salvo no banco com sucesso!")

    except Exception as e:
        print(f"❌ DEU ERRO: {e}")
        db.rollback()
    finally:
        db.close()

# --- AQUI É ONDE O PROBLEMA GERALMENTE ESTÁ ---
print("6. Chegou no final do arquivo. Verificando __name__...")
if __name__ == "__main__":
    print("7. Iniciando a execução principal!")
    update_prices()
else:
    print(f"⚠️ O script foi importado, mas não executado. __name__ é: {__name__}")