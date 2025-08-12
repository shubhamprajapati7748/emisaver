from app.crud.crud_market_loan import market_loan
from app.database.session import SessionLocal
from app.core.logger import logger
from typing import List, Optional
from app.database.models.market_loan import MarketLoan
from sqlalchemy.orm import Session

class MarketLoanService:
    def __init__(self):
        self.crud_market_loan = market_loan

    def get_by_query(self, db: Session, query : str) -> List[MarketLoan]:
        """Get market loans by query.
        
        Args:
            db (Session): The database session.
            query (str): The query to get market loans.
            
        Returns:
            List[MarketLoan]: The list of market loans.
        """
        try:        
            logger.info(f"Getting market loans by query: {query}")
            return self.crud_market_loan.get_by_query(db, query)
        except Exception as e:
            logger.error(f"Error getting market loans by query: {e}")
            return []
    
    def get_by_loan_type(self, db: Session, loan_type: str) -> List[MarketLoan]:
        """Get market loans by loan type.
        
        Args:
            db (Session): The database session.
            loan_type (str): The loan type to get market loans.
            
        Returns:
            List[MarketLoan]: The list of market loans.
        """
        try:
            logger.info(f"Getting market loans by loan type: {loan_type}")
            return self.crud_market_loan.get_by_loan_type(db, loan_type)
        except Exception as e:
            logger.error(f"Error getting market loans by loan type: {e}")
            return []
    
    def get_by_loan_type_and_amount(self, db: Session, loan_type: str, amount: float) -> List[MarketLoan]:
        """Get market loans by loan type and amount.
        
        Args:
            db (Session): The database session.
            loan_type (str): The loan type to get market loans.
            amount (float): The amount to get market loans.
            
        Returns:
            List[MarketLoan]: The list of market loans.
        """
        try:
            logger.info(f"Getting market loans by loan type and amount: {loan_type}, {amount}")
            return self.crud_market_loan.get_by_loan_type_and_amount(db, loan_type, amount)
        except Exception as e:
            logger.error(f"Error getting market loans by loan type and amount: {e}")
            return []
    
    def get_by_loan_type_and_amount_and_interest_rate_and_tenure(self, db: Session, loan_type: str, amount: float, interest_rate: float, tenure: int, lender_name: Optional[str] = None) -> List[MarketLoan]:
        """Get market loans by loan type, amount and tenure.
        
        Args:
            db (Session): The database session.
            loan_type (str): The loan type to get market loans.
            amount (float): The amount to get market loans.
            interest_rate (float): The interest rate to get market loans.
            tenure (int): The tenure to get market loans.
            lender_name (Optional[str]): The lender name to get market loans.
            
        Returns:
            List[MarketLoan]: The list of market loans.
        """
        try:
            logger.info(f"Getting market loans by loan type, amount and tenure and interest rate: {loan_type}, {amount}, {interest_rate}, {tenure}, {lender_name} ...")
            return self.crud_market_loan.get_by_loan_type_and_amount_and_interest_rate_and_tenure(db, loan_type, amount, interest_rate, tenure, lender_name)
        except Exception as e:
            logger.error(f"Error getting market loans by loan type, amount and tenure and interest rate: {e}")
            return []
    
market_loan_service = MarketLoanService()