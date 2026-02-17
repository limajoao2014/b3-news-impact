# scripts/seed_watchlist.py

from app.db import sessionLocal
from app.models import Company

watchlist = [
    ("VALE3", "Vale", "Mineração"),
    ("ITUB4", "Itaú Unibanco", "Bancos"),
    ("PETR4", "Petrobras PN", "Petróleo"),
    ("AXIA3", "Axioma", "Industrial"),
    ("PETR3", "Petrobras ON", "Petróleo"),
    ("BBDC4", "Bradesco PN", "Bancos"),
    ("SBSP3", "Sabesp", "Saneamento"),
    ("BPAC11", "BTG Pactual", "Bancos"),
    ("WEGE3", "WEG", "Industrial"),
    ("B3SA3", "B3", "Financeiro")
]

db = sessionLocal()

for ticker, name, sector in watchlist:
    exists = db.query(Company).filter(Company.ticker == ticker).first()
    if not exists:
        db.add(Company(ticker=ticker, name=name, sector=sector))

db.commit()
db.close()

print("Watchlist inserida com sucesso.")
