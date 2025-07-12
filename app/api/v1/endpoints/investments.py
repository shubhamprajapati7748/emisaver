from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.services import investment_service
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class InvestmentCreate(BaseModel):
    user_id: int
    investment_id: Optional[str] = None
    investment_type: Optional[str] = None
    institution: Optional[str] = None
    amount_invested: Optional[int] = None
    current_value: Optional[int] = None
    start_date: Optional[datetime] = None
    maturity_date: Optional[datetime] = None


class InvestmentUpdate(BaseModel):
    investment_id: Optional[str] = None
    investment_type: Optional[str] = None
    institution: Optional[str] = None
    amount_invested: Optional[int] = None
    current_value: Optional[int] = None
    start_date: Optional[datetime] = None
    maturity_date: Optional[datetime] = None


@router.post("/")
async def create_investment(
    investment_data: InvestmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new investment."""
    try:
        result = investment_service.create_investment(db, investment_data.dict())
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{investment_id}")
async def get_investment(investment_id: int, db: Session = Depends(get_db)):
    """Get investment by ID."""
    try:
        result = investment_service.get_investment(db, investment_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Investment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}")
async def get_investments_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all investments for a user."""
    try:
        result = investment_service.get_investments_by_user(db, user_id)
        return {"investments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/institution/{institution}")
async def get_investments_by_institution(institution: str, db: Session = Depends(get_db)):
    """Get all investments from a specific institution."""
    try:
        result = investment_service.get_investments_by_institution(db, institution)
        return {"investments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/type/{investment_type}")
async def get_investments_by_type(investment_type: str, db: Session = Depends(get_db)):
    """Get all investments of a specific type."""
    try:
        result = investment_service.get_investments_by_type(db, investment_type)
        return {"investments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matured")
async def get_matured_investments(db: Session = Depends(get_db)):
    """Get all matured investments."""
    try:
        result = investment_service.get_matured_investments(db)
        return {"investments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profitable")
async def get_profitable_investments(db: Session = Depends(get_db)):
    """Get investments where current value > amount invested."""
    try:
        result = investment_service.get_profitable_investments(db)
        return {"investments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-value")
async def get_high_value_investments(
    min_value: int = Query(100000, description="Minimum investment value"),
    db: Session = Depends(get_db)
):
    """Get investments with current value above threshold."""
    try:
        result = investment_service.get_high_value_investments(db, min_value)
        return {"investments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{investment_id}")
async def update_investment(
    investment_id: int,
    update_data: InvestmentUpdate,
    db: Session = Depends(get_db)
):
    """Update investment."""
    try:
        result = investment_service.update_investment(db, investment_id, update_data.dict(exclude_unset=True))
        if result and result["success"]:
            return result
        elif result and not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        else:
            raise HTTPException(status_code=404, detail="Investment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{investment_id}")
async def delete_investment(investment_id: int, db: Session = Depends(get_db)):
    """Delete investment."""
    try:
        success = investment_service.delete_investment(db, investment_id)
        if success:
            return {"message": "Investment deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Investment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/total-value")
async def get_total_investment_value_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get total current value of investments for a user."""
    try:
        result = investment_service.get_total_investment_value_by_user(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/summary")
async def get_investments_summary(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive summary of user's investments."""
    try:
        result = investment_service.get_investments_summary(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/analytics")
async def get_investment_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get investment analytics for a user."""
    try:
        result = investment_service.get_investment_analytics(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 