from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.crud_user import user as crud_user
from app.crud.crud_bank_account import bank_account as crud_bank_account
from app.crud.crud_loan import loan as crud_loan
from app.crud.crud_investment import investment as crud_investment
from app.schemas.user_details import UserInfo
from app.core.logger import logger
from app.schemas.response import BaseResponse


class UserService:
    def __init__(self):
        self.crud_user = crud_user
        self.crud_bank_account = crud_bank_account
        self.crud_loan = crud_loan
        self.crud_investment = crud_investment
    
    async def store_user_info_from_fi_mcp(self, db: Session, user_info: UserInfo) -> Dict[str, Any]:
        """Store user info from FiMCP response.
        
        Args:
            db (Session) : The database session.
            user_info (UserInfo) : The user info from FiMCP.

        Returns:
            Dict[str, Any] : The result of the operation.

        Raises:
            Exception : If an error occurs while creating the user.
        """
        try:
            # Validate user data
            user_data = user_info.user if hasattr(user_info, 'user') else user_info.get('user', {})
            if not user_data:
                logger.error("No user data found in UserInfo")
                return {
                    "success": False,
                    "message": "No user data found",
                    "error": "User data is missing"
                }
            
            # Convert user data to dict if it's a Pydantic model
            if hasattr(user_data, 'model_dump'):
                user_data = user_data.model_dump()
            elif hasattr(user_data, 'dict'):
                user_data = user_data.dict()
            
            logger.info(f"Processing user data: {user_data}")
            
            # Check if user already exists
            existing_user = self.crud_user.get_by_email(db, user_data['email'])
            if existing_user:
                logger.info(f"User with email {user_data['email']} already exists")
                return BaseResponse(
                    status="error",
                    message="User already exists",
                    data=user_info
                )

            # Create user
            try:
                user = self.crud_user.create(db, obj_in=user_data)
                logger.info(f"Created user with ID: {user.id}")
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")
                raise e
            
            # Store bank accounts
            bank_accounts_created = []
            bank_accounts = user_info.bank_accounts if hasattr(user_info, 'bank_accounts') else user_info.get('bank_accounts', [])
            if bank_accounts:
                logger.info(f"Processing {len(bank_accounts)} bank accounts")
                for i, bank_data in enumerate(bank_accounts):
                    try:
                        # Convert to dict if it's a Pydantic model
                        if hasattr(bank_data, 'model_dump'):
                            bank_data = bank_data.model_dump()
                        elif hasattr(bank_data, 'dict'):
                            bank_data = bank_data.dict()
                        
                        bank_data["user_id"] = user.id
                        logger.info(f"Creating bank account {i+1}: {bank_data}")
                        bank_account = self.crud_bank_account.create(db, obj_in=bank_data)
                        bank_accounts_created.append(bank_account)
                        logger.info(f"Created bank account: {bank_account.id} for bank: {bank_data.get('bank_name', 'Unknown')}")
                    except Exception as e:
                        logger.error(f"Error creating bank account {i+1}: {str(e)}")
                        raise e
            else:
                logger.info("No bank accounts found in response")
            
            # Store loans
            loans_created = []
            loans = user_info.loans if hasattr(user_info, 'loans') else user_info.get('loans', [])
            if loans:
                logger.info(f"Processing {len(loans)} loans")
                for i, loan_data in enumerate(loans):
                    try:
                        # Convert to dict if it's a Pydantic model
                        if hasattr(loan_data, 'model_dump'):
                            loan_data = loan_data.model_dump()
                        elif hasattr(loan_data, 'dict'):
                            loan_data = loan_data.dict()
                        
                        loan_data["user_id"] = user.id
                        logger.info(f"Creating loan {i+1}: {loan_data}")
                        loan = self.crud_loan.create(db, obj_in=loan_data)
                        loans_created.append(loan)
                        logger.info(f"Created loan: {loan.id} for lender: {loan_data.get('lender', 'Unknown')}")
                    except Exception as e:
                        logger.error(f"Error creating loan {i+1}: {str(e)}")
                        raise e
            else:
                logger.info("No loans found in response")
            
            # Store investments
            investments_created = []
            investments = user_info.investments if hasattr(user_info, 'investments') else user_info.get('investments', [])
            if investments:
                logger.info(f"Processing {len(investments)} investments")
                for i, investment_data in enumerate(investments):
                    try:
                        # Convert to dict if it's a Pydantic model
                        if hasattr(investment_data, 'model_dump'):
                            investment_data = investment_data.model_dump()
                        elif hasattr(investment_data, 'dict'):
                            investment_data = investment_data.dict()
                        
                        investment_data["user_id"] = user.id
                        logger.info(f"Creating investment {i+1}: {investment_data}")
                        investment = self.crud_investment.create(db, obj_in=investment_data)
                        investments_created.append(investment)
                        logger.info(f"Created investment: {investment.id} for institution: {investment_data.get('institution', 'Unknown')}")
                    except Exception as e:
                        logger.error(f"Error creating investment {i+1}: {str(e)}")
                        raise e
            else:
                logger.info("No investments found in response")
            
            logger.info(f"Successfully stored user info from FiMCP for user {user.id} with {len(bank_accounts_created)} bank accounts, {len(loans_created)} loans, and {len(investments_created)} investments")
            
            return BaseResponse(
                status="success",
                message="User info fetched and stored successfully",
                data=user_info
            )
            
        except Exception as e:
            logger.error(f"Error storing user info from FiMCP: {str(e)}")
            db.rollback()
            raise e
        
    def get_user_details_by_phone(self, db: Session, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get user details by phone number."""
        try:
            logger.info(f"Getting user details by phone number: {phone_number}")
            user = self.crud_user.get_by_phone(db, phone_number)
            if not user:
                return None
            return self.get_user(db, user.id)
        
        except Exception as e:
            logger.error(f"Error getting user details by phone number {phone_number}: {str(e)}")
            raise e
        
    def get_all_users(self, db: Session) -> List[Dict[str, Any]]:
        """Get all users."""
        try:
            users = self.crud_user.get_multi(db, skip=0, limit=100, filters=None)
            return [user.to_dict() for user in users]
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
    
    def get_user(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user with all related data."""
        try:
            user = self.crud_user.get_user_with_relationships(db, user_id)
            if not user:
                return None
            
            return {
                "user": user.to_dict(),
                "bank_accounts": [bank_account.to_dict() for bank_account in user.bank_accounts],
                "loans": [loan.to_dict() for loan in user.loans],
                "investments": [investment.to_dict() for investment in user.investments]
            }
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {str(e)}")
            raise e
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email with all related data."""
        try:
            user = self.crud_user.get_by_email(db, email)
            if not user:
                return None
            
            return self.get_user(db, user.id)
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            raise e
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get multiple users with optional filtering."""
        try:
            users = self.crud_user.get_multi(db, skip=skip, limit=limit, filters=filters)
            return [{"user": user} for user in users]
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}")
            raise e
    
    def update_user(self, db: Session, user_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user data."""
        try:
            user = self.crud_user.get(db, user_id)
            if not user:
                return None
            
            updated_user = self.crud_user.update(db, db_obj=user, obj_in=update_data)
            return {"user": updated_user}
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise e
    
    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete user and all related data."""
        try:
            user = self.crud_user.get(db, user_id)
            if not user:
                return False
            
            self.crud_user.delete(db, user_id=user_id)
            logger.info(f"Deleted user {user_id} and all related data")
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise e
    
    def get_user_financial_summary(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get comprehensive financial summary for a user."""
        try:
            user = self.crud_user.get(db, user_id)
            if not user:
                return None
            
            # Get all related data
            bank_accounts = self.crud_bank_account.get_by_user_id(db, user_id)
            loans = self.crud_loan.get_by_user_id(db, user_id)
            investments = self.crud_investment.get_by_user_id(db, user_id)
            
            # Calculate totals
            total_bank_balance = sum(account.balance or 0 for account in bank_accounts)
            total_loan_liability = sum(loan.current_balance or 0 for loan in loans)
            total_investment_value = sum(investment.current_value or 0 for investment in investments)
            
            # Calculate net worth
            total_assets = total_bank_balance + total_investment_value
            net_worth = total_assets - total_loan_liability
            
            return {
                "user_id": user_id,
                "user_name": user.full_name,
                "total_bank_balance": total_bank_balance,
                "total_loan_liability": total_loan_liability,
                "total_investment_value": total_investment_value,
                "total_assets": total_assets,
                "net_worth": net_worth,
                "bank_accounts_count": len(bank_accounts),
                "loans_count": len(loans),
                "investments_count": len(investments),
                "cibil_score": user.cibil_score
            }
        except Exception as e:
            logger.error(f"Error getting financial summary for user {user_id}: {str(e)}")
            raise e
    
    def update_user_financial_summary(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Update user's financial summary based on current data."""
        try:
            updated_user = self.crud_user.update_financial_summary(db, user_id)
            if not updated_user:
                return None
            
            return {"user": updated_user}
        except Exception as e:
            logger.error(f"Error updating financial summary for user {user_id}: {str(e)}")
            raise e


user_service = UserService()
