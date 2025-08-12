from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.models.loan_request import LoanRequest
from datetime import datetime
import uuid


class CRUDLoanRequest:
    def get(self, db: Session, loan_request_id: uuid.UUID) -> Optional[LoanRequest]:
        """Get loan request by ID."""
        return db.query(LoanRequest).filter(LoanRequest.id == loan_request_id).first()
    
    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> List[LoanRequest]:
        """Get all loan requests for a user."""
        return db.query(LoanRequest).filter(LoanRequest.user_id == user_id).all()
    
    def get_by_from_loan_id(self, db: Session, from_loan_id: str) -> Optional[LoanRequest]:  
        """Get loan request by from_loan_id field."""
        return db.query(LoanRequest).filter(LoanRequest.from_loan_id == from_loan_id).first()
    
    def get_by_to_loan_id(self, db: Session, to_loan_id: str) -> Optional[LoanRequest]:  
        """Get loan request by to_loan_id field."""
        return db.query(LoanRequest).filter(LoanRequest.to_loan_id == to_loan_id).first()
    
    def get_by_status(self, db: Session, status: str) -> List[LoanRequest]:
        """Get all loan requests with a specific status."""
        return db.query(LoanRequest).filter(LoanRequest.status == status).all()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[LoanRequest]:
        """Get multiple loan requests with optional filtering."""
        query = db.query(LoanRequest)
        
        if filters:
            for field, value in filters.items():
                if hasattr(LoanRequest, field) and value is not None:
                    if isinstance(value, str):
                        query = query.filter(getattr(LoanRequest, field).ilike(f"%{value}%"))
                    else:
                        query = query.filter(getattr(LoanRequest, field) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> LoanRequest:
        """Create a new loan request."""
        db_obj = LoanRequest(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: LoanRequest, 
        obj_in: Dict[str, Any]
    ) -> LoanRequest:
        """Update loan request."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, loan_request_id: uuid.UUID) -> bool:
        """Delete loan request."""
        obj = db.query(LoanRequest).get(loan_request_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
    
   
    def get_by_query(self, db: Session, queryFilter: str) -> List[LoanRequest]:
        """Get loans by query filter.
        
        Args:
            db (Session): The database session.
            queryFilter (str): The query filter to apply.
            
        Returns:
            List[Loan]: List of loans matching the query.
        """
        # This is a simple implementation - in production, you'd want to parse the query
        # more carefully to avoid SQL injection
        return db.query(LoanRequest).filter(queryFilter).all()


loan_request = CRUDLoanRequest()
