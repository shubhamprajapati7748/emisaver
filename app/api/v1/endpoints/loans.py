from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.services import loan_service
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class LoanCreate(BaseModel):
    user_id: int
    loan_id: Optional[str] = None
    lender: Optional[str] = None
    loan_type: Optional[str] = None
    original_amount: Optional[int] = None
    current_balance: Optional[int] = None
    interest_rate: Optional[float] = None
    tenure_months: Optional[int] = None
    emi_amount: Optional[int] = None
    status: Optional[str] = None
    open_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    account_number: Optional[str] = None
    collateral_value: Optional[int] = None
    prepayment_penalty: Optional[int] = None


class LoanUpdate(BaseModel):
    loan_id: Optional[str] = None
    lender: Optional[str] = None
    loan_type: Optional[str] = None
    original_amount: Optional[int] = None
    current_balance: Optional[int] = None
    interest_rate: Optional[float] = None
    tenure_months: Optional[int] = None
    emi_amount: Optional[int] = None
    status: Optional[str] = None
    open_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    account_number: Optional[str] = None
    collateral_value: Optional[int] = None
    prepayment_penalty: Optional[int] = None


@router.post("/")
async def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
):
    """Create a new loan."""
    try:
        result = loan_service.create_loan(db, loan_data.dict())
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{loan_id}")
async def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """Get loan by ID."""
    try:
        result = loan_service.get_loan(db, loan_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Loan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}")
async def get_loans_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all loans for a user."""
    try:
        result = loan_service.get_loans_by_user(db, user_id)
        return {"loans": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/active")
async def get_active_loans_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all active loans for a user."""
    try:
        result = loan_service.get_active_loans_by_user(db, user_id)
        return {"loans": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overdue")
async def get_overdue_loans(db: Session = Depends(get_db)):
    """Get all overdue loans."""
    try:
        result = loan_service.get_overdue_loans(db)
        return {"loans": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lender/{lender}")
async def get_loans_by_lender(lender: str, db: Session = Depends(get_db)):
    """Get all loans from a specific lender."""
    try:
        result = loan_service.get_loans_by_lender(db, lender)
        return {"loans": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/type/{loan_type}")
async def get_loans_by_type(loan_type: str, db: Session = Depends(get_db)):
    """Get all loans of a specific type."""
    try:
        result = loan_service.get_loans_by_type(db, loan_type)
        return {"loans": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-interest")
async def get_high_interest_loans(
    min_interest_rate: float = Query(10.0, description="Minimum interest rate"),
    db: Session = Depends(get_db)
):
    """Get loans with interest rate above threshold."""
    try:
        result = loan_service.get_high_interest_loans(db, min_interest_rate)
        return {"loans": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{loan_id}")
async def update_loan(
    loan_id: int,
    update_data: LoanUpdate,
    db: Session = Depends(get_db)
):
    """Update loan."""
    try:
        result = loan_service.update_loan(db, loan_id, update_data.dict(exclude_unset=True))
        if result and result["success"]:
            return result
        elif result and not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        else:
            raise HTTPException(status_code=404, detail="Loan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{loan_id}")
async def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """Delete loan."""
    try:
        success = loan_service.delete_loan(db, loan_id)
        if success:
            return {"message": "Loan deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Loan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/total-liability")
async def get_total_liability_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get total loan liability for a user."""
    try:
        result = loan_service.get_total_liability_by_user(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/summary")
async def get_loans_summary(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive summary of user's loans."""
    try:
        result = loan_service.get_loans_summary(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/analytics")
async def get_loan_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get loan analytics for a user."""
    try:
        result = loan_service.get_loan_analytics(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 