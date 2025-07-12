from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.database.models.bank_account import BankAccount
from datetime import datetime
import uuid


class CRUDBankAccount:
    def get(self, db: Session, bank_account_id: uuid.UUID) -> Optional[BankAccount]:
        """Get bank account by ID."""
        return db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    
    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> List[BankAccount]:
        """Get all bank accounts for a user."""
        return db.query(BankAccount).filter(BankAccount.user_id == user_id).all()
    
    def get_by_account_number(self, db: Session, account_number: str) -> Optional[BankAccount]:
        """Get bank account by account number."""
        return db.query(BankAccount).filter(BankAccount.account_number == account_number).first()
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[BankAccount]:
        """Get multiple bank accounts with optional filtering."""
        query = db.query(BankAccount)
        
        if filters:
            for field, value in filters.items():
                if hasattr(BankAccount, field) and value is not None:
                    if isinstance(value, str):
                        query = query.filter(getattr(BankAccount, field).ilike(f"%{value}%"))
                    else:
                        query = query.filter(getattr(BankAccount, field) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> BankAccount:
        """Create a new bank account."""
        db_obj = BankAccount(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: BankAccount, 
        obj_in: Dict[str, Any]
    ) -> BankAccount:
        """Update bank account."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, bank_account_id: uuid.UUID) -> BankAccount:
        """Delete bank account."""
        obj = db.query(BankAccount).get(bank_account_id)
        db.delete(obj)
        db.commit()
        return obj
    
    def exists(self, db: Session, bank_account_id: uuid.UUID) -> bool:
        """Check if bank account exists."""
        return db.query(BankAccount).filter(BankAccount.id == bank_account_id).first() is not None
    
    def get_total_balance_by_user(self, db: Session, user_id: uuid.UUID) -> float:
        """Get total balance across all bank accounts for a user."""
        accounts = self.get_by_user_id(db, user_id)
        total_balance = sum(account.balance or 0 for account in accounts)
        return total_balance
    
    def get_accounts_by_bank(self, db: Session, bank_name: str) -> List[BankAccount]:
        """Get all accounts for a specific bank."""
        return db.query(BankAccount).filter(BankAccount.bank_name == bank_name).all()
    
    def get_accounts_by_type(self, db: Session, account_type: str) -> List[BankAccount]:
        """Get all accounts of a specific type."""
        return db.query(BankAccount).filter(BankAccount.account_type == account_type).all()


bank_account = CRUDBankAccount()
