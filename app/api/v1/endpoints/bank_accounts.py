from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.services import bank_account_service
from pydantic import BaseModel

router = APIRouter()


class BankAccountCreate(BaseModel):
    user_id: int
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[int] = None
    ifsc_code: Optional[str] = None


class BankAccountUpdate(BaseModel):
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[int] = None
    ifsc_code: Optional[str] = None


@router.post("/")
async def create_bank_account(
    bank_account_data: BankAccountCreate,
    db: Session = Depends(get_db)
):
    """Create a new bank account."""
    try:
        result = bank_account_service.create_bank_account(db, bank_account_data.dict())
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{bank_account_id}")
async def get_bank_account(bank_account_id: int, db: Session = Depends(get_db)):
    """Get bank account by ID."""
    try:
        result = bank_account_service.get_bank_account(db, bank_account_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Bank account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}")
async def get_bank_accounts_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all bank accounts for a user."""
    try:
        result = bank_account_service.get_bank_accounts_by_user(db, user_id)
        return {"bank_accounts": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bank/{bank_name}")
async def get_bank_accounts_by_bank(bank_name: str, db: Session = Depends(get_db)):
    """Get all accounts for a specific bank."""
    try:
        result = bank_account_service.get_bank_accounts_by_bank(db, bank_name)
        return {"bank_accounts": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/type/{account_type}")
async def get_bank_accounts_by_type(account_type: str, db: Session = Depends(get_db)):
    """Get all accounts of a specific type."""
    try:
        result = bank_account_service.get_bank_accounts_by_type(db, account_type)
        return {"bank_accounts": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{bank_account_id}")
async def update_bank_account(
    bank_account_id: int,
    update_data: BankAccountUpdate,
    db: Session = Depends(get_db)
):
    """Update bank account."""
    try:
        result = bank_account_service.update_bank_account(db, bank_account_id, update_data.dict(exclude_unset=True))
        if result and result["success"]:
            return result
        elif result and not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        else:
            raise HTTPException(status_code=404, detail="Bank account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{bank_account_id}")
async def delete_bank_account(bank_account_id: int, db: Session = Depends(get_db)):
    """Delete bank account."""
    try:
        success = bank_account_service.delete_bank_account(db, bank_account_id)
        if success:
            return {"message": "Bank account deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Bank account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/total-balance")
async def get_total_balance_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get total balance across all bank accounts for a user."""
    try:
        result = bank_account_service.get_total_balance_by_user(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/summary")
async def get_bank_accounts_summary(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive summary of user's bank accounts."""
    try:
        result = bank_account_service.get_bank_accounts_summary(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 