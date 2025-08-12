from app.database.models.market_loan import MarketLoan
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

class CRUDMarketLoan:

    def get_by_query(self, db: Session, queryFilter: str) -> List[MarketLoan]:
        """Get loans by query filter.
        
        Args:
            db (Session): The database session.
            queryFilter (str): The query filter to apply.
            
        Returns:
            List[Loan]: List of loans matching the query.
        """
        # This is a simple implementation - in production, you'd want to parse the query
        # more carefully to avoid SQL injection
        return db.query(MarketLoan).filter(queryFilter).all()

    def get_by_loan_type(self, db: Session, loan_type: str) -> List[MarketLoan]:
        """Get loans by loan type.
        
        Args:
            db (Session): The database session.
            loan_type (str): The loan type to filter by.
            
        Returns:
            List[Loan]: List of loans matching the loan type.
        """
        return db.query(MarketLoan).filter(MarketLoan.loan_type == loan_type).all()
    
    def get_by_loan_type_and_amount(self, db: Session, loan_type: str, amount: float) -> List[MarketLoan]:
        """Get loans by loan type and amount.
        
        Args:
            db (Session): The database session.
            loan_type (str): The loan type to filter by.
            amount (float): The amount to filter by.
            
        Returns:    
            List[Loan]: List of loans matching the loan type and amount.
        """
        return db.query(MarketLoan).filter(MarketLoan.loan_type == loan_type, MarketLoan.min_loan_amount <= amount, MarketLoan.max_loan_amount >= amount).all()
    
    def get_by_loan_type_and_amount_and_interest_rate_and_tenure(self, db: Session, loan_type: str, amount: float, interest_rate: float, tenure: int, lender_name: Optional[str] = None) -> List[MarketLoan]:
        """Get loans by loan type, amount and tenure.

        Args:
            db (Session): The database session. 
            loan_type (str): The loan type to filter by.
            amount (float): The amount to filter by.
            interest_rate (float): The interest rate to filter by.
            tenure (int): The tenure to filter by.
            lender_name (str): The lender name to filter by.
            
        Returns:
            List[Loan]: List of loans matching the loan type, amount and tenure.
        """
        if lender_name is not None:
            return db.query(MarketLoan).filter(func.lower(MarketLoan.loan_type).ilike(f"%{loan_type.lower()}%"), MarketLoan.min_loan_amount <= amount, MarketLoan.max_loan_amount >= amount, MarketLoan.roi_start <= interest_rate, MarketLoan.roi_end >= interest_rate, MarketLoan.tenure_upto >= tenure, func.lower(MarketLoan.lender_name).ilike(f"%{lender_name.lower()}%")).order_by(MarketLoan.roi_start.asc()).limit(5).all()
        else:
            return db.query(MarketLoan).filter(func.lower(MarketLoan.loan_type).ilike(f"%{loan_type.lower()}%"), MarketLoan.min_loan_amount <= amount, MarketLoan.max_loan_amount >= amount, MarketLoan.roi_start <= interest_rate, MarketLoan.roi_end >= interest_rate, MarketLoan.tenure_upto >= tenure).order_by(MarketLoan.roi_start.asc()).limit(5).all()
    


market_loan = CRUDMarketLoan()