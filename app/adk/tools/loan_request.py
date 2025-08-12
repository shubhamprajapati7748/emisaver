from app.services.loan_request_service import loan_request_service
from app.database.session import SessionLocal
from typing import Dict, Any, Optional
from app.core.logger import logger
import uuid


def save_new_loan_request_tool(user_id: str, loan_id: str, loan_type: str) -> Dict[str, Any]:
    """
    Save a new loan request by the user to the database.

    Args:
        user_id: The ID of the user making the loan request. (e.g. 550e8400-e29b-41d4-a716-446655440002)
        loan_id: The ID of the loan being selected by the user. (e.g. 123e4567-e89b-12d3-a456-426614174000)
        loan_type: The type of loan being requested. (e.g. Personal)

    Returns:
        A dictionary containing the success status, message and loan request details otherwise error message e.g. {
            "success": True,
            "message": "Loan request created successfully",
            "loan_request_id": "123e4567-e89b-12d3-a456-426614174000",
        } 
        or
        {
            "success": False,
            "message": "Error in save_new_loan_request_tool",
            "loan_request_id": "123e4567-e89b-12d3-a456-426614174000",
        }
    """
    db = SessionLocal()
    try:
        logger.info(f"save_new_loan_request_tool called for user_id: {user_id}, loan_id: {loan_id}, loan_type: {loan_type} ...")
        response = loan_request_service.create_loan_request(db, user_id, "new_loan", loan_type, None, loan_id)
        logger.info(f"save_new_loan_request_tool response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in save_new_loan_request_tool: {e}")
        return {
            "success": False,
            "message": "Error in save_new_loan_request_tool"
        }
    finally:
        db.close()


def save_switch_loan_request_tool(user_id: str, loan_type: str, from_loan_id: Optional[str], to_loan_id: str) -> Dict[str, Any]: 
    """
    Save a new loan request by the user to the database.

    The LLM should parse the user_id, request_type, loan_type, from_loan_id and to_loan_id.

    Args:
        user_id: The ID of the user making the loan request. (e.g. 550e8400-e29b-41d4-a716-446655440002)
        loan_type: The type of loan being requested. (e.g. personal)
        from_loan_id: The ID of the loan being switched from. (e.g. 123e4567-e89b-12d3-a456-426614174000)
        to_loan_id: The ID of the loan selected by the user for switched to (e.g. 123e4567-e89b-12d3-a456-426614174000)

    Returns: 
        A dictionary containing the success status, message and loan request details otherwise error message e.g. {
            "success": True,
            "message": "Loan request created successfully",
            "loan_request_id": "123e4567-e89b-12d3-a456-426614174000",
        } 
        or
        {
            "success": False,
            "message": "To loan already exists",
            "loan_request_id": "123e4567-e89b-12d3-a456-426614174000",
        }
    """
    db = SessionLocal()
    try:
        logger.info(f"save_switch_loan_request_tool called for user_id: {user_id}, loan_type: {loan_type}, from_loan_id: {from_loan_id}, to_loan_id: {to_loan_id} ...")
        user_id_uuid = uuid.UUID(user_id)
        to_loan_id_uuid = uuid.UUID(to_loan_id)
        from_loan_id_uuid = uuid.UUID(from_loan_id)
        
        response = loan_request_service.create_loan_request(db, user_id_uuid, "switch_loan", loan_type, from_loan_id_uuid, to_loan_id_uuid)
        logger.info(f"save_switch_loan_request_tool response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in save_switch_loan_request_tool: {e}")
        return { "success": False, "message": "Error in save_switch_loan_request_tool", "error": str(e) }
    finally:
        db.close()