from typing import List, Optional, Dict, Any
from app.crud.crud_loan import loan as crud_loan
from app.crud.crud_user import user as crud_user
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.logger import logger


class LoanService:
    def __init__(self):
        self.crud_loan = crud_loan
        self.crud_user = crud_user
    
    def create_loan(self, db: Session, loan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new loan."""
        try:
            # Validate user exists
            user = self.crud_user.get(db, loan_data.get("user_id"))
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            # Check if loan_id already exists
            if loan_data.get("loan_id"):
                existing_loan = self.crud_loan.get_by_loan_id(db, loan_data["loan_id"])
                if existing_loan:
                    return {
                        "success": False,
                        "message": "Loan with this loan ID already exists"
                    }
            
            # Create loan
            loan = self.crud_loan.create(db, obj_in=loan_data)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, loan_data["user_id"])
            
            logger.info(f"Created loan {loan.id} for user {loan_data['user_id']}")
            
            return {
                "success": True,
                "message": "Loan created successfully",
                "loan": loan
            }
            
        except Exception as e:
            logger.error(f"Error creating loan: {str(e)}")
            db.rollback()
            raise e
    
    def get_loan(self, db: Session, loan_id: int) -> Optional[Dict[str, Any]]:
        """Get loan by ID."""
        try:
            loan = self.crud_loan.get(db, loan_id)
            if not loan:
                return None
            
            return {"loan": loan}
        except Exception as e:
            logger.error(f"Error getting loan {loan_id}: {str(e)}")
            raise e
    
    def get_loans_by_user(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all loans for a user."""
        try:
            loans = self.crud_loan.get_by_user_id(db, user_id)
            return [{"loan": loan} for loan in loans]
        except Exception as e:
            logger.error(f"Error getting loans for user {user_id}: {str(e)}")
            raise e
    
    def get_active_loans_by_user(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all active loans for a user."""
        try:
            loans = self.crud_loan.get_active_loans_by_user(db, user_id)
            return [{"loan": loan} for loan in loans]
        except Exception as e:
            logger.error(f"Error getting active loans for user {user_id}: {str(e)}")
            raise e
    
    def get_overdue_loans(self, db: Session) -> List[Dict[str, Any]]:
        """Get all overdue loans."""
        try:
            loans = self.crud_loan.get_overdue_loans(db)
            return [{"loan": loan} for loan in loans]
        except Exception as e:
            logger.error(f"Error getting overdue loans: {str(e)}")
            raise e
    
    def get_loans_by_lender(self, db: Session, lender: str) -> List[Dict[str, Any]]:
        """Get all loans from a specific lender."""
        try:
            loans = self.crud_loan.get_by_lender(db, lender)
            return [{"loan": loan} for loan in loans]
        except Exception as e:
            logger.error(f"Error getting loans for lender {lender}: {str(e)}")
            raise e
    
    def get_loans_by_type(self, db: Session, loan_type: str) -> List[Dict[str, Any]]:
        """Get all loans of a specific type."""
        try:
            loans = self.crud_loan.get_loans_by_type(db, loan_type)
            return [{"loan": loan} for loan in loans]
        except Exception as e:
            logger.error(f"Error getting loans of type {loan_type}: {str(e)}")
            raise e
    
    def get_high_interest_loans(self, db: Session, min_interest_rate: float = 10.0) -> List[Dict[str, Any]]:
        """Get loans with interest rate above threshold."""
        try:
            loans = self.crud_loan.get_high_interest_loans(db, min_interest_rate)
            return [{"loan": loan} for loan in loans]
        except Exception as e:
            logger.error(f"Error getting high interest loans: {str(e)}")
            raise e
    
    def update_loan(self, db: Session, loan_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update loan."""
        try:
            loan = self.crud_loan.get(db, loan_id)
            if not loan:
                return None
            
            # If loan_id is being updated, check for duplicates
            if "loan_id" in update_data and update_data["loan_id"] != loan.loan_id:
                existing_loan = self.crud_loan.get_by_loan_id(db, update_data["loan_id"])
                if existing_loan:
                    return {
                        "success": False,
                        "message": "Loan with this loan ID already exists"
                    }
            
            updated_loan = self.crud_loan.update(db, db_obj=loan, obj_in=update_data)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, loan.user_id)
            
            return {
                "success": True,
                "message": "Loan updated successfully",
                "loan": updated_loan
            }
        except Exception as e:
            logger.error(f"Error updating loan {loan_id}: {str(e)}")
            raise e
    
    def delete_loan(self, db: Session, loan_id: int) -> bool:
        """Delete loan."""
        try:
            loan = self.crud_loan.get(db, loan_id)
            if not loan:
                return False
            
            user_id = loan.user_id
            self.crud_loan.delete(db, loan_id=loan_id)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, user_id)
            
            logger.info(f"Deleted loan {loan_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting loan {loan_id}: {str(e)}")
            raise e
    
    def get_total_liability_by_user(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get total loan liability for a user."""
        try:
            total_liability = self.crud_loan.get_total_liability_by_user(db, user_id)
            loans = self.crud_loan.get_by_user_id(db, user_id)
            
            return {
                "user_id": user_id,
                "total_liability": total_liability,
                "loan_count": len(loans),
                "loans": loans
            }
        except Exception as e:
            logger.error(f"Error getting total liability for user {user_id}: {str(e)}")
            raise e
    
    def get_loans_summary(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get comprehensive summary of user's loans."""
        try:
            loans = self.crud_loan.get_by_user_id(db, user_id)
            if not loans:
                return {
                    "user_id": user_id,
                    "total_liability": 0,
                    "loan_count": 0,
                    "loans_by_lender": {},
                    "loans_by_type": {},
                    "loans_by_status": {}
                }
            
            total_liability = sum(loan.current_balance or 0 for loan in loans)
            
            # Group by lender
            loans_by_lender = {}
            for loan in loans:
                lender = loan.lender or "Unknown"
                if lender not in loans_by_lender:
                    loans_by_lender[lender] = []
                loans_by_lender[lender].append(loan)
            
            # Group by loan type
            loans_by_type = {}
            for loan in loans:
                loan_type = loan.loan_type or "Unknown"
                if loan_type not in loans_by_type:
                    loans_by_type[loan_type] = []
                loans_by_type[loan_type].append(loan)
            
            # Group by status
            loans_by_status = {}
            for loan in loans:
                status = loan.status or "Unknown"
                if status not in loans_by_status:
                    loans_by_status[status] = []
                loans_by_status[status].append(loan)
            
            return {
                "user_id": user_id,
                "total_liability": total_liability,
                "loan_count": len(loans),
                "loans_by_lender": loans_by_lender,
                "loans_by_type": loans_by_type,
                "loans_by_status": loans_by_status,
                "loans": loans
            }
        except Exception as e:
            logger.error(f"Error getting loans summary for user {user_id}: {str(e)}")
            raise e
    
    def get_loan_analytics(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get loan analytics for a user."""
        try:
            loans = self.crud_loan.get_by_user_id(db, user_id)
            if not loans:
                return {
                    "user_id": user_id,
                    "total_loans": 0,
                    "active_loans": 0,
                    "overdue_loans": 0,
                    "total_emi": 0,
                    "average_interest_rate": 0,
                    "total_liability": 0
                }
            
            active_loans = [loan for loan in loans if loan.status == "active"]
            overdue_loans = [loan for loan in loans if loan.due_date and loan.due_date < datetime.now()]
            
            total_emi = sum(loan.emi_amount or 0 for loan in loans)
            total_liability = sum(loan.current_balance or 0 for loan in loans)
            
            # Calculate average interest rate
            interest_rates = [loan.interest_rate for loan in loans if loan.interest_rate]
            average_interest_rate = sum(interest_rates) / len(interest_rates) if interest_rates else 0
            
            return {
                "user_id": user_id,
                "total_loans": len(loans),
                "active_loans": len(active_loans),
                "overdue_loans": len(overdue_loans),
                "total_emi": total_emi,
                "average_interest_rate": round(average_interest_rate, 2),
                "total_liability": total_liability,
                "loans": loans
            }
        except Exception as e:
            logger.error(f"Error getting loan analytics for user {user_id}: {str(e)}")
            raise e


loan_service = LoanService()
