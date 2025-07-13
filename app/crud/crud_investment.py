from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.models.investment import Investment
from datetime import datetime
import uuid


class CRUDInvestment:
    def get(self, db: Session, investment_id: uuid.UUID) -> Optional[Investment]:
        """Get investment by ID."""
        return db.query(Investment).filter(Investment.id == investment_id).first()
    
    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> List[Investment]:
        """Get all investments for a user."""
        return db.query(Investment).filter(Investment.user_id == user_id).all()
    
    def get_by_investment_id(self, db: Session, investment_id: str) -> Optional[Investment]:
        """Get investment by investment_id field."""
        return db.query(Investment).filter(Investment.investment_id == investment_id).first()
    
    def get_by_institution(self, db: Session, institution: str) -> List[Investment]:
        """Get all investments from a specific institution."""
        return db.query(Investment).filter(Investment.institution == institution).all()
    
    def get_by_type(self, db: Session, investment_type: str) -> List[Investment]:
        """Get all investments of a specific type."""
        return db.query(Investment).filter(Investment.investment_type == investment_type).all()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Investment]:
        """Get multiple investments with optional filtering."""
        query = db.query(Investment)
        
        if filters:
            for field, value in filters.items():
                if hasattr(Investment, field) and value is not None:
                    if isinstance(value, str):
                        query = query.filter(getattr(Investment, field).ilike(f"%{value}%"))
                    else:
                        query = query.filter(getattr(Investment, field) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> Investment:
        """Create a new investment."""
        db_obj = Investment(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: Investment, 
        obj_in: Dict[str, Any]
    ) -> Investment:
        """Update investment."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, investment_id: uuid.UUID) -> bool:
        """Delete investment."""
        obj = db.query(Investment).get(investment_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
    
    def is_exists(self, db: Session, investment_id: uuid.UUID) -> bool:
        """Check if investment exists."""
        return db.query(Investment).filter(Investment.id == investment_id).first() is not None
    
    def get_total_investment_value_by_user(self, db: Session, user_id: uuid.UUID) -> float:
        """Get total current value of investments for a user."""
        investments = self.get_by_user_id(db, user_id)
        total_value = sum(investment.current_value or 0 for investment in investments)
        return total_value
    
    def get_matured_investments(self, db: Session) -> List[Investment]:
        """Get all matured investments."""
        current_date = datetime.now()
        return db.query(Investment).filter(
            and_(
                Investment.maturity_date < current_date,
                Investment.current_value > 0
            )
        ).all()
    
    def get_profitable_investments(self, db: Session) -> List[Investment]:
        """Get investments where current value > amount invested."""
        return db.query(Investment).filter(
            Investment.current_value > Investment.amount_invested
        ).all()
    
    def get_investments_by_date_range(
        self, 
        db: Session, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Investment]:
        """Get investments started within a date range."""
        return db.query(Investment).filter(
            and_(
                Investment.start_date >= start_date,
                Investment.start_date <= end_date
            )
        ).all()
    
    def get_high_value_investments(self, db: Session, min_value: float = 100000) -> List[Investment]:
        """Get investments with current value above threshold."""
        return db.query(Investment).filter(Investment.current_value > min_value).all()


investment = CRUDInvestment()
