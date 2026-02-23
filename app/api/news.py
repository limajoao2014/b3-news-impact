from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db import SessionLocal
from app.models import News, Company

router = APIRouter()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
class NewsResponse(BaseModel):
    id: int
    title: str
    sentiment: Optional[str] = "Neutro"
    impact_score: Optional[int] = 0
    published_at: datetime
    source: str
    company_name: Optional[str] = "Geral"
    class config:
        from_attributes = True

@router.get("/", response_model=List[NewsResponse])
def read_news(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    "Retorna a lista de noticias analisadas, da mais recente para a mais antiga"

    results = (
        db.query(News)
        .join(Company, News.company_id == Company.id, isouter=True) 
        .order_by(News.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    response = []
    for news in results:
        comp_name = news.company.name if news.company else "Geral"
        response.append(NewsResponse(
            id=news.id,
            title=news.title,
            sentiment=news.sentiment or "Neutro",
            impact_score=news.impact_score or 0,
            published_at=news.published_at,
            source=news.source,
            company_name=comp_name
        ))

    return response