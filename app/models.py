from sqlalchemy  import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import base 

class Company(base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)

    prices = relationship("Price", back_populates="company")
    news = relationship("News", back_populates="company")   


class Price(base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    close = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    collected_at = Column(DateTime, default=datetime.utcnow)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="prices")


class News(base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, index=True)
    title = Column(String)
    source = Column(String)
    url = Column(String, unique=True)
    snippet = Column(Text)
    published_at = Column(DateTime)
    hash_dedupe = Column(String, unique=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="news")


class Analysis(base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"))
    sentiment = Column(String)
    impact_level = Column(String)
    time_horizon = Column(String)
    summary = Column(Text)
    topics_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)