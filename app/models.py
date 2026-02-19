from sqlalchemy  import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base 

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)

    # Relacionamento: Uma empresa tem muitos preços
    prices = relationship("Price", back_populates="company")

    news = relationship("News", back_populates="company")
    #analysis = relationship("Analysis", back_populates="company")

# --- ADICIONE ESTA CLASSE NOVA ---
class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id")) # Link com a empresa
    price = Column(Float)  # Preço de fechamento
    date = Column(DateTime, default=datetime.utcnow) # Data da coleta

    # Relacionamento de volta
    company = relationship("Company", back_populates="prices")

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True) # Pode ser null se for notícia geral
    title = Column(String)
    summary = Column(Text)
    url = Column(String, unique=True) # Evita notícias duplicadas
    source = Column(String) # Ex: "InfoMoney"
    published_at = Column(DateTime)
    
    # Campos que a IA vai preencher depois
    sentiment = Column(String, nullable=True) # Positivo/Negativo
    impact_score = Column(Integer, nullable=True) # 1 a 5

    company = relationship("Company", back_populates="news")


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True)
    # news_id = Column(Integer, ForeignKey("news.id"))
    sentiment = Column(String)
    impact_level = Column(String)
    time_horizon = Column(String)
    summary = Column(Text)
    topics_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)