import sys
import os
import yfinance as yf

# Setup para importar os módulos da pasta 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db import SessionLocal
from app.models import Company, Price

def seed_historical_prices():
    db = SessionLocal()
    
    companies = db.query(Company).all()
    if not companies:
        print("❌ Nenhuma empresa encontrada no banco.")
        return

    print("⏳ Iniciando o download de histórico (Último 1 mês)...")

    for company in companies:
        # No Yahoo Finance, as ações do Brasil precisam terminar com ".SA" (ex: PETR4.SA)
        yf_ticker = f"{company.ticker}.SA"
        print(f"   📊 Baixando {yf_ticker}...")
        
        try:
            stock = yf.Ticker(yf_ticker)
            # Você pode mudar period="1mo" para "6mo" (6 meses) ou "1y" (1 ano) se quiser mais dados!
            hist = stock.history(period="1mo") 
            
            if hist.empty:
                print(f"      ⚠️ Nenhum dado encontrado para {yf_ticker}")
                continue
            
            count = 0
            for date_index, row in hist.iterrows():
                # Converte a data do Pandas para o formato do Python e remove o fuso horário
                clean_date = date_index.to_pydatetime().replace(tzinfo=None)
                
                # Pegamos o preço de Fechamento (Close) do dia
                close_price = float(row['Close'])
                
                # Salva no banco de dados
                new_price = Price(
                    company_id=company.id,
                    price=close_price,
                    date=clean_date
                )
                db.add(new_price)
                count += 1
                
            db.commit()
            print(f"      ✅ Sucesso! {count} dias salvos para {company.ticker}.")
            
        except Exception as e:
            print(f"      ❌ Erro em {company.ticker}: {e}")
            db.rollback()

    db.close()
    print("🏁 Importação de histórico finalizada!")

if __name__ == "__main__":
    seed_historical_prices()