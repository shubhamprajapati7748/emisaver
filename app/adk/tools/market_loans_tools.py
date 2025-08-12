from app.services.market_loan_service import market_loan_service
from app.database.session import SessionLocal
from app.core.logger import logger
from typing import Dict, Any, List, Optional

def get_available_market_loans_tool(loan_type: str = "Personal", amount: float = 100000.0, interest_rate: float = 10.5, tenure: int = 1, lender_name: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Get the information about market loans based on the provided loan type, amount and tenure.
    
    The LLM should parse the loan type, amount and tenure.

    Args:
        loan_type: The type of loan. (e.g. Personal, Home, Car, Business)
        amount: The amount of loan. (e.g. 100000, 200000, 300000, 400000, 500000)
        interest_rate: The interest rate of the loan. (e.g. 9, 10.5, 11.5, 12.5, 13.5, 14.5)
        tenure: The tenure of the loan in years (e.g. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        lender_name: The name of the lender. (e.g. HDFC Bank, ICICI Bank etc.) if not provided, leave it empty string ''.

    Returns:
        A list of dictionaries containing market loan information if found, otherwise None.
    """
    db = SessionLocal()
    try:
        logger.info(f"Getting market loans info for loan type: {loan_type}, amount: {amount}, interest_rate: {interest_rate}, tenure: {tenure} years, lender_name: {lender_name} ...")

        market_loans = market_loan_service.get_by_loan_type_and_amount_and_interest_rate_and_tenure(db, loan_type, amount, interest_rate, tenure, lender_name)
        
        if len(market_loans) == 0:
            logger.warning(f"No market loans found for loan type: {loan_type}, amount: {amount}, tenure: {tenure} years")
            return None

        # Convert market loans to dictionary format
        market_loans_info = []
        for loan in market_loans:
            loan_info = {
                "loan_id": str(loan.id) if loan.id else None,
                "lender_name": loan.lender_name if loan.lender_name else None,
                "loan_type": loan.loan_type if loan.loan_type else None,
                "roi_start": loan.roi_start if loan.roi_start else None,
                "roi_end": loan.roi_end if loan.roi_end else None,
                "min_loan_amount": loan.min_loan_amount if loan.min_loan_amount else None,
                "max_loan_amount": loan.max_loan_amount if loan.max_loan_amount else None,
                "tenure_upto": loan.tenure_upto if loan.tenure_upto else None,
                "loan_tags": loan.loan_tags if loan.loan_tags else None,
                "status": loan.status if loan.status else None,
                "processing_fee": loan.processing_fee if loan.processing_fee else None,
                "prepayment_penalty": loan.prepayment_penalty if loan.prepayment_penalty else None,
                "offer_valid_till": loan.offer_valid_till if loan.offer_valid_till else None,
                "eligibility_criteria": loan.eligibility_criteria if loan.eligibility_criteria else None,
                "terms_and_conditions": loan.terms_and_conditions if loan.terms_and_conditions else None
            }
            market_loans_info.append(loan_info)

        return market_loans_info

    except Exception as e:
        logger.error(f"Error getting market loans info for loan type: {loan_type}, amount: {amount}, tenure: {tenure}: {e}")
        return None
    finally:
        db.close()