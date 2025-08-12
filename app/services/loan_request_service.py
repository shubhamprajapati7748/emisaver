from app.crud.crud_loan_request import loan_request
from app.crud.crud_user import user
import uuid
from app.core.logger import logger
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

class LoanRequestService:
    def __init__(self):
        self.crud_loan_request = loan_request
        self.crud_user = user

    def create_loan_request(self, db: Session, user_id: uuid.UUID, request_type: str, loan_type: str, from_loan_id: Optional[uuid.UUID], to_loan_id: uuid.UUID) -> Dict[str, Any]:
        logger.info(f"Creating loan request for user {user_id}...")
        # Validate user exists
        user = self.crud_user.get(db, user_id)
        if not user:
            return {
                "success": False,
                "message": "User not found"
            }
        
        # Validate loan exists 
        existing_loan_request = self.crud_loan_request.get_by_to_loan_id(db, to_loan_id)
        if existing_loan_request:
            return {
                "success": False,
                "message": "To loan already exists",
                "loan_request_id": str(existing_loan_request.id)
            }
        
        loan_request_data = {
            "user_id": user_id,
            "request_type": request_type,
            "loan_type": loan_type,
            "from_loan_id": from_loan_id,
            "to_loan_id": to_loan_id
        }

        # store loan request
        new_loan_request = self.crud_loan_request.create(db, obj_in=loan_request_data)
        logger.info(f"Loan request created successfully for user {user_id}")
        return {
            "success": True,
            "message": "Loan request created successfully",
            "loan_request_id": str(new_loan_request.id)
        }
        
loan_request_service = LoanRequestService()