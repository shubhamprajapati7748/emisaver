from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.mcp.fi_mcp import FiMCP
from app.schemas.user_details import UserInfo
from app.api.deps import get_fi_mcp
from app.database.session import get_db
from app.services.user_service import user_service
from app.core.logger import logger
from typing import Dict, Any
from app.schemas.response import BaseResponse

router = APIRouter()

@router.get("/")
async def get_users():
    """Get all users."""
    return {"message": "Users fetched successfully"}

@router.post("/user-info")
async def user_info(fi_mcp: FiMCP = Depends(get_fi_mcp), db: Session = Depends(get_db)):
    """Get user info from Fi MCP and store in database."""
    try:
        logger.info("Fetching user info from Fi MCP...")
        response = await fi_mcp.get_user_info()
        # response = {'user': {'full_name': 'Ramesh Kumar', 'email': 'ramesh.kumar@example.com', 'phone_number': '+919876543210', 'cibil_score': 807, 'total_assets': 227908.0, 'total_liabilities': 1195.0, 'net_worth': 226713.0}, 'bank_accounts': [{'bank_name': 'ICICI Bank', 'account_number': 'XXXXXXXX5479', 'account_type': 'savings', 'balance': 948.4, 'ifsc_code': 'ICIC0006312'}, {'bank_name': 'State Bank of India', 'account_number': 'XXXXXXXXXXXXX9754', 'account_type': 'savings', 'balance': 21034.76, 'ifsc_code': 'SBIN0007483'}], 'loans': [{'loan_id': 'PVT3090001', 'lender': 'ICICI Bank', 'loan_type': 'credit_card', 'original_amount': 41229.0, 'current_balance': 1195.0, 'interest_rate': 3.5, 'tenure_months': 0, 'emi_amount': 0.0, 'status': 'Active', 'open_date': '2024-05-22', 'due_date': '2025-07-15', 'account_number': 'PVT3090001', 'collateral_value': 0.0, 'prepayment_penalty': 0.0}], 'investments': [{'investment_id': '8b5647de-7bd6-4124-b9cf-a19f4ad82114', 'investment_type': 'etf', 'institution': 'CDSL', 'amount_invested': 85000.0, 'current_value': 97568.92, 'start_date': '2023-01-15', 'maturity_date': None}, {'investment_id': 'a31580d7-2949-461c-a897-3d3dab34b64f', 'investment_type': 'stock', 'institution': 'CDSL', 'amount_invested': 50000.0, 'current_value': 57537.85, 'start_date': '2022-11-20', 'maturity_date': None}, {'investment_id': 'EPF-12345', 'investment_type': 'epf', 'institution': "Employees' Provident Fund Organisation", 'amount_invested': 45000.0, 'current_value': 50820.0, 'start_date': '2021-08-01', 'maturity_date': None}]}
        logger.info(f"User info fetched from Fi MCP: {response}")
        # Check if response is a string (login required) or UserInfo object
        if isinstance(response, str):
            logger.info("Login is required")
            return BaseResponse(
                status="error",
                message="Login is required",
                data=response
            )
        elif isinstance(response, UserInfo):
            return await _process_user_info(response, db)
        elif isinstance(response, dict):
            # Handle case where response is a dictionary
            logger.info("Response is a dictionary, attempting to convert to UserInfo...")
            try:
                user_info_obj = UserInfo(**response)
                return await _process_user_info(user_info_obj, db)
            except Exception as e:
                logger.error(f"Error converting dictionary to UserInfo: {str(e)}")
                return BaseResponse(
                    status="error",
                    message="Error converting response to UserInfo",
                    data=response
                )
        else:
            logger.error(f"Unexpected response type: {type(response)}")
            return BaseResponse(
                status="error",
                message="Unexpected response type from Fi MCP",
                data=response
            )
    except Exception as e:
        logger.error(f"Error in user_info endpoint: {str(e)}")
        return BaseResponse(
            status="error",
            message="Error fetching or storing user info",
            data=str(e)
        )

async def _process_user_info(user_info: UserInfo, db: Session) -> Dict[str, Any]:
    """Helper function to process UserInfo object and store in database."""
    # Validate that the response has all required data
    has_user = user_info.user is not None
    has_bank_accounts = len(user_info.bank_accounts) > 0
    has_investments = len(user_info.investments) > 0
    has_loans = len(user_info.loans) > 0
    
    logger.info(f"Data validation - User: {has_user}, Bank Accounts: {has_bank_accounts}, Investments: {has_investments}, Loans: {has_loans}")
    
    # Check if we have at least user data and one other category
    if has_user and (has_bank_accounts or has_investments or has_loans):
        logger.info("Response contains valid user data, storing user info in database...")
        # Store user info in database
        result = await user_service.store_user_info_from_fi_mcp(db, user_info)
        logger.warning("User info stored in database successfully.")
        return result
    else:
        logger.warning("Response does not contain sufficient user data")
        return BaseResponse(
            status="error",
            message="Insufficient user info received",
            data=user_info   
        )
