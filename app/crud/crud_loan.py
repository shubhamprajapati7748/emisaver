from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.models.loan import Loan
from datetime import datetime
import uuid


class CRUDLoan:
    def get(self, db: Session, loan_id: uuid.UUID) -> Optional[Loan]:
        """Get loan by ID."""
        return db.query(Loan).filter(Loan.id == loan_id).first()
    
    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> List[Loan]:
        """Get all loans for a user."""
        return db.query(Loan).filter(Loan.user_id == user_id).all()
    
    def get_by_loan_id(self, db: Session, loan_id: str) -> Optional[Loan]:
        """Get loan by loan_id field."""
        return db.query(Loan).filter(Loan.loan_id == loan_id).first()
    
    def get_by_lender(self, db: Session, lender: str) -> List[Loan]:
        """Get all loans from a specific lender."""
        return db.query(Loan).filter(Loan.lender == lender).all()
    
    def get_by_status(self, db: Session, status: str) -> List[Loan]:
        """Get all loans with a specific status."""
        return db.query(Loan).filter(Loan.status == status).all()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Loan]:
        """Get multiple loans with optional filtering."""
        query = db.query(Loan)
        
        if filters:
            for field, value in filters.items():
                if hasattr(Loan, field) and value is not None:
                    if isinstance(value, str):
                        query = query.filter(getattr(Loan, field).ilike(f"%{value}%"))
                    else:
                        query = query.filter(getattr(Loan, field) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> Loan:
        """Create a new loan."""
        db_obj = Loan(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: Loan, 
        obj_in: Dict[str, Any]
    ) -> Loan:
        """Update loan."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, loan_id: uuid.UUID) -> Loan:
        """Delete loan."""
        obj = db.query(Loan).get(loan_id)
        db.delete(obj)
        db.commit()
        return obj
    
    def exists(self, db: Session, loan_id: uuid.UUID) -> bool:
        """Check if loan exists."""
        return db.query(Loan).filter(Loan.id == loan_id).first() is not None
    
    def get_total_liability_by_user(self, db: Session, user_id: uuid.UUID) -> float:
        """Get total loan liability for a user."""
        loans = self.get_by_user_id(db, user_id)
        total_liability = sum(loan.current_balance or 0 for loan in loans)
        return total_liability
    
    def get_active_loans_by_user(self, db: Session, user_id: uuid.UUID) -> List[Loan]:
        """Get all active loans for a user."""
        return db.query(Loan).filter(
            and_(
                Loan.user_id == user_id,
                Loan.status == "active"
            )
        ).all()
    
    def get_overdue_loans(self, db: Session) -> List[Loan]:
        """Get all overdue loans."""
        current_date = datetime.now()
        return db.query(Loan).filter(
            and_(
                Loan.due_date < current_date,
                Loan.status == "active"
            )
        ).all()
    
    def get_loans_by_type(self, db: Session, loan_type: str) -> List[Loan]:
        """Get all loans of a specific type."""
        return db.query(Loan).filter(Loan.loan_type == loan_type).all()
    
    def get_high_interest_loans(self, db: Session, min_interest_rate: float = 10.0) -> List[Loan]:
        """Get loans with interest rate above threshold."""
        return db.query(Loan).filter(Loan.interest_rate > min_interest_rate).all()


loan = CRUDLoan()
