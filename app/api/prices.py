from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db import SessionLocal
from app.models import Company, Price

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PriceResponse(BaseModel):
    id: int
    ticker: str
    price: float
    company_name: Optional[str] = "Geral"
    date: datetime # <-- Mudei de timestamp para date (como está no banco)

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PriceResponse])
def read_prices(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    results = (
        db.query(Price)
        .join(Company, Price.company_id == Company.id, isouter=True)
        .order_by(Price.date.desc()) # <-- Mudei de Price.timestamp para Price.date
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    response = []
    for price in results:
        comp_name = price.company.name if price.company else "Geral"
        
        # Pega o ticker da empresa (se a empresa existir, senão deixa vazio)
        comp_ticker = price.company.ticker if price.company else "N/A" 
        
        response.append(PriceResponse(
            id=price.id,
            ticker=comp_ticker, # <-- Pegando do comp_ticker que criamos acima
            price=price.price,
            company_name=comp_name,
            date=price.date # <-- Mudei de price.timestamp para price.date
        ))
        
    return response