from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.crud_bank_account import bank_account as crud_bank_account
from app.crud.crud_user import user as crud_user
import logging

logger = logging.getLogger(__name__)


class BankAccountService:
    def __init__(self):
        self.crud_bank_account = crud_bank_account
        self.crud_user = crud_user
    
    def create_bank_account(self, db: Session, bank_account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new bank account."""
        try:
            # Validate user exists
            user = self.crud_user.get(db, bank_account_data.get("user_id"))
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            # Check if account number already exists
            if bank_account_data.get("account_number"):
                existing_account = self.crud_bank_account.get_by_account_number(
                    db, bank_account_data["account_number"]
                )
                if existing_account:
                    return {
                        "success": False,
                        "message": "Bank account with this account number already exists"
                    }
            
            # Create bank account
            bank_account = self.crud_bank_account.create(db, obj_in=bank_account_data)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, bank_account_data["user_id"])
            
            logger.info(f"Created bank account {bank_account.id} for user {bank_account_data['user_id']}")
            
            return {
                "success": True,
                "message": "Bank account created successfully",
                "bank_account": bank_account
            }
            
        except Exception as e:
            logger.error(f"Error creating bank account: {str(e)}")
            db.rollback()
            raise e
    
    def get_bank_account(self, db: Session, bank_account_id: int) -> Optional[Dict[str, Any]]:
        """Get bank account by ID."""
        try:
            bank_account = self.crud_bank_account.get(db, bank_account_id)
            if not bank_account:
                return None
            
            return {"bank_account": bank_account}
        except Exception as e:
            logger.error(f"Error getting bank account {bank_account_id}: {str(e)}")
            raise e
    
    def get_bank_accounts_by_user(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all bank accounts for a user."""
        try:
            bank_accounts = self.crud_bank_account.get_by_user_id(db, user_id)
            return [{"bank_account": account} for account in bank_accounts]
        except Exception as e:
            logger.error(f"Error getting bank accounts for user {user_id}: {str(e)}")
            raise e
    
    def get_bank_accounts_by_bank(self, db: Session, bank_name: str) -> List[Dict[str, Any]]:
        """Get all accounts for a specific bank."""
        try:
            bank_accounts = self.crud_bank_account.get_accounts_by_bank(db, bank_name)
            return [{"bank_account": account} for account in bank_accounts]
        except Exception as e:
            logger.error(f"Error getting bank accounts for bank {bank_name}: {str(e)}")
            raise e
    
    def get_bank_accounts_by_type(self, db: Session, account_type: str) -> List[Dict[str, Any]]:
        """Get all accounts of a specific type."""
        try:
            bank_accounts = self.crud_bank_account.get_accounts_by_type(db, account_type)
            return [{"bank_account": account} for account in bank_accounts]
        except Exception as e:
            logger.error(f"Error getting bank accounts of type {account_type}: {str(e)}")
            raise e
    
    def update_bank_account(self, db: Session, bank_account_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update bank account."""
        try:
            bank_account = self.crud_bank_account.get(db, bank_account_id)
            if not bank_account:
                return None
            
            # If account number is being updated, check for duplicates
            if "account_number" in update_data and update_data["account_number"] != bank_account.account_number:
                existing_account = self.crud_bank_account.get_by_account_number(
                    db, update_data["account_number"]
                )
                if existing_account:
                    return {
                        "success": False,
                        "message": "Bank account with this account number already exists"
                    }
            
            updated_account = self.crud_bank_account.update(db, db_obj=bank_account, obj_in=update_data)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, bank_account.user_id)
            
            return {
                "success": True,
                "message": "Bank account updated successfully",
                "bank_account": updated_account
            }
        except Exception as e:
            logger.error(f"Error updating bank account {bank_account_id}: {str(e)}")
            raise e
    
    def delete_bank_account(self, db: Session, bank_account_id: int) -> bool:
        """Delete bank account."""
        try:
            bank_account = self.crud_bank_account.get(db, bank_account_id)
            if not bank_account:
                return False
            
            user_id = bank_account.user_id
            self.crud_bank_account.delete(db, bank_account_id=bank_account_id)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, user_id)
            
            logger.info(f"Deleted bank account {bank_account_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting bank account {bank_account_id}: {str(e)}")
            raise e
    
    def get_total_balance_by_user(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get total balance across all bank accounts for a user."""
        try:
            total_balance = self.crud_bank_account.get_total_balance_by_user(db, user_id)
            bank_accounts = self.crud_bank_account.get_by_user_id(db, user_id)
            
            return {
                "user_id": user_id,
                "total_balance": total_balance,
                "account_count": len(bank_accounts),
                "accounts": bank_accounts
            }
        except Exception as e:
            logger.error(f"Error getting total balance for user {user_id}: {str(e)}")
            raise e
    
    def get_bank_accounts_summary(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get comprehensive summary of user's bank accounts."""
        try:
            bank_accounts = self.crud_bank_account.get_by_user_id(db, user_id)
            if not bank_accounts:
                return {
                    "user_id": user_id,
                    "total_balance": 0,
                    "account_count": 0,
                    "accounts_by_bank": {},
                    "accounts_by_type": {}
                }
            
            total_balance = sum(account.balance or 0 for account in bank_accounts)
            
            # Group by bank
            accounts_by_bank = {}
            for account in bank_accounts:
                bank_name = account.bank_name or "Unknown"
                if bank_name not in accounts_by_bank:
                    accounts_by_bank[bank_name] = []
                accounts_by_bank[bank_name].append(account)
            
            # Group by account type
            accounts_by_type = {}
            for account in bank_accounts:
                account_type = account.account_type or "Unknown"
                if account_type not in accounts_by_type:
                    accounts_by_type[account_type] = []
                accounts_by_type[account_type].append(account)
            
            return {
                "user_id": user_id,
                "total_balance": total_balance,
                "account_count": len(bank_accounts),
                "accounts_by_bank": accounts_by_bank,
                "accounts_by_type": accounts_by_type,
                "accounts": bank_accounts
            }
        except Exception as e:
            logger.error(f"Error getting bank accounts summary for user {user_id}: {str(e)}")
            raise e


bank_account_service = BankAccountService()
