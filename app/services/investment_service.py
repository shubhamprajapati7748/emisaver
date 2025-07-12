from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.crud_investment import investment as crud_investment
from app.crud.crud_user import user as crud_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class InvestmentService:
    def __init__(self):
        self.crud_investment = crud_investment
        self.crud_user = crud_user
    
    def create_investment(self, db: Session, investment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new investment."""
        try:
            # Validate user exists
            user = self.crud_user.get(db, investment_data.get("user_id"))
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            # Check if investment_id already exists
            if investment_data.get("investment_id"):
                existing_investment = self.crud_investment.get_by_investment_id(
                    db, investment_data["investment_id"]
                )
                if existing_investment:
                    return {
                        "success": False,
                        "message": "Investment with this investment ID already exists"
                    }
            
            # Create investment
            investment = self.crud_investment.create(db, obj_in=investment_data)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, investment_data["user_id"])
            
            logger.info(f"Created investment {investment.id} for user {investment_data['user_id']}")
            
            return {
                "success": True,
                "message": "Investment created successfully",
                "investment": investment
            }
            
        except Exception as e:
            logger.error(f"Error creating investment: {str(e)}")
            db.rollback()
            raise e
    
    def get_investment(self, db: Session, investment_id: int) -> Optional[Dict[str, Any]]:
        """Get investment by ID."""
        try:
            investment = self.crud_investment.get(db, investment_id)
            if not investment:
                return None
            
            return {"investment": investment}
        except Exception as e:
            logger.error(f"Error getting investment {investment_id}: {str(e)}")
            raise e
    
    def get_investments_by_user(self, db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all investments for a user."""
        try:
            investments = self.crud_investment.get_by_user_id(db, user_id)
            return [{"investment": investment} for investment in investments]
        except Exception as e:
            logger.error(f"Error getting investments for user {user_id}: {str(e)}")
            raise e
    
    def get_investments_by_institution(self, db: Session, institution: str) -> List[Dict[str, Any]]:
        """Get all investments from a specific institution."""
        try:
            investments = self.crud_investment.get_by_institution(db, institution)
            return [{"investment": investment} for investment in investments]
        except Exception as e:
            logger.error(f"Error getting investments for institution {institution}: {str(e)}")
            raise e
    
    def get_investments_by_type(self, db: Session, investment_type: str) -> List[Dict[str, Any]]:
        """Get all investments of a specific type."""
        try:
            investments = self.crud_investment.get_by_type(db, investment_type)
            return [{"investment": investment} for investment in investments]
        except Exception as e:
            logger.error(f"Error getting investments of type {investment_type}: {str(e)}")
            raise e
    
    def get_matured_investments(self, db: Session) -> List[Dict[str, Any]]:
        """Get all matured investments."""
        try:
            investments = self.crud_investment.get_matured_investments(db)
            return [{"investment": investment} for investment in investments]
        except Exception as e:
            logger.error(f"Error getting matured investments: {str(e)}")
            raise e
    
    def get_profitable_investments(self, db: Session) -> List[Dict[str, Any]]:
        """Get investments where current value > amount invested."""
        try:
            investments = self.crud_investment.get_profitable_investments(db)
            return [{"investment": investment} for investment in investments]
        except Exception as e:
            logger.error(f"Error getting profitable investments: {str(e)}")
            raise e
    
    def get_high_value_investments(self, db: Session, min_value: int = 100000) -> List[Dict[str, Any]]:
        """Get investments with current value above threshold."""
        try:
            investments = self.crud_investment.get_high_value_investments(db, min_value)
            return [{"investment": investment} for investment in investments]
        except Exception as e:
            logger.error(f"Error getting high value investments: {str(e)}")
            raise e
    
    def update_investment(self, db: Session, investment_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update investment."""
        try:
            investment = self.crud_investment.get(db, investment_id)
            if not investment:
                return None
            
            # If investment_id is being updated, check for duplicates
            if "investment_id" in update_data and update_data["investment_id"] != investment.investment_id:
                existing_investment = self.crud_investment.get_by_investment_id(
                    db, update_data["investment_id"]
                )
                if existing_investment:
                    return {
                        "success": False,
                        "message": "Investment with this investment ID already exists"
                    }
            
            updated_investment = self.crud_investment.update(db, db_obj=investment, obj_in=update_data)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, investment.user_id)
            
            return {
                "success": True,
                "message": "Investment updated successfully",
                "investment": updated_investment
            }
        except Exception as e:
            logger.error(f"Error updating investment {investment_id}: {str(e)}")
            raise e
    
    def delete_investment(self, db: Session, investment_id: int) -> bool:
        """Delete investment."""
        try:
            investment = self.crud_investment.get(db, investment_id)
            if not investment:
                return False
            
            user_id = investment.user_id
            self.crud_investment.delete(db, investment_id=investment_id)
            
            # Update user's financial summary
            self.crud_user.update_financial_summary(db, user_id)
            
            logger.info(f"Deleted investment {investment_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting investment {investment_id}: {str(e)}")
            raise e
    
    def get_total_investment_value_by_user(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get total current value of investments for a user."""
        try:
            total_value = self.crud_investment.get_total_investment_value_by_user(db, user_id)
            investments = self.crud_investment.get_by_user_id(db, user_id)
            
            return {
                "user_id": user_id,
                "total_value": total_value,
                "investment_count": len(investments),
                "investments": investments
            }
        except Exception as e:
            logger.error(f"Error getting total investment value for user {user_id}: {str(e)}")
            raise e
    
    def get_investments_summary(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get comprehensive summary of user's investments."""
        try:
            investments = self.crud_investment.get_by_user_id(db, user_id)
            if not investments:
                return {
                    "user_id": user_id,
                    "total_value": 0,
                    "total_invested": 0,
                    "total_profit": 0,
                    "investment_count": 0,
                    "investments_by_institution": {},
                    "investments_by_type": {}
                }
            
            total_value = sum(investment.current_value or 0 for investment in investments)
            total_invested = sum(investment.amount_invested or 0 for investment in investments)
            total_profit = total_value - total_invested
            
            # Group by institution
            investments_by_institution = {}
            for investment in investments:
                institution = investment.institution or "Unknown"
                if institution not in investments_by_institution:
                    investments_by_institution[institution] = []
                investments_by_institution[institution].append(investment)
            
            # Group by investment type
            investments_by_type = {}
            for investment in investments:
                investment_type = investment.investment_type or "Unknown"
                if investment_type not in investments_by_type:
                    investments_by_type[investment_type] = []
                investments_by_type[investment_type].append(investment)
            
            return {
                "user_id": user_id,
                "total_value": total_value,
                "total_invested": total_invested,
                "total_profit": total_profit,
                "profit_percentage": round((total_profit / total_invested * 100) if total_invested > 0 else 0, 2),
                "investment_count": len(investments),
                "investments_by_institution": investments_by_institution,
                "investments_by_type": investments_by_type,
                "investments": investments
            }
        except Exception as e:
            logger.error(f"Error getting investments summary for user {user_id}: {str(e)}")
            raise e
    
    def get_investment_analytics(self, db: Session, user_id: int) -> Optional[Dict[str, Any]]:
        """Get investment analytics for a user."""
        try:
            investments = self.crud_investment.get_by_user_id(db, user_id)
            if not investments:
                return {
                    "user_id": user_id,
                    "total_investments": 0,
                    "matured_investments": 0,
                    "profitable_investments": 0,
                    "total_value": 0,
                    "total_invested": 0,
                    "total_profit": 0,
                    "average_return_rate": 0
                }
            
            matured_investments = [inv for inv in investments if inv.maturity_date and inv.maturity_date < datetime.now()]
            profitable_investments = [inv for inv in investments if inv.current_value and inv.amount_invested and inv.current_value > inv.amount_invested]
            
            total_value = sum(inv.current_value or 0 for inv in investments)
            total_invested = sum(inv.amount_invested or 0 for inv in investments)
            total_profit = total_value - total_invested
            
            # Calculate average return rate
            return_rates = []
            for inv in investments:
                if inv.amount_invested and inv.amount_invested > 0 and inv.current_value:
                    rate = ((inv.current_value - inv.amount_invested) / inv.amount_invested) * 100
                    return_rates.append(rate)
            
            average_return_rate = sum(return_rates) / len(return_rates) if return_rates else 0
            
            return {
                "user_id": user_id,
                "total_investments": len(investments),
                "matured_investments": len(matured_investments),
                "profitable_investments": len(profitable_investments),
                "total_value": total_value,
                "total_invested": total_invested,
                "total_profit": total_profit,
                "profit_percentage": round((total_profit / total_invested * 100) if total_invested > 0 else 0, 2),
                "average_return_rate": round(average_return_rate, 2),
                "investments": investments
            }
        except Exception as e:
            logger.error(f"Error getting investment analytics for user {user_id}: {str(e)}")
            raise e


investment_service = InvestmentService()
