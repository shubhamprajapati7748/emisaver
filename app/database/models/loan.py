

from sqlalchemy import Integer, String, ForeignKey, Float, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import datetime
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.database.models.user import User

class Loan(Base):
    __tablename__ = "loans"

    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    loan_id : Mapped[str] = mapped_column(String(500), nullable=True)
    lender : Mapped[str] = mapped_column(String(500), nullable=True)
    loan_type : Mapped[str] = mapped_column(String(500), nullable=True)
    original_amount : Mapped[float] = mapped_column(Float, nullable=True)
    current_balance : Mapped[float] = mapped_column(Float, nullable=True)
    interest_rate : Mapped[float] = mapped_column(Float, nullable=True)
    tenure_months : Mapped[int] = mapped_column(Integer, nullable=True)
    emi_amount : Mapped[float] = mapped_column(Float, nullable=True)
    status : Mapped[str] = mapped_column(String(500), nullable=True)
    open_date : Mapped[str] = mapped_column(String(500), nullable=True)
    due_date : Mapped[str] = mapped_column(String(500), nullable=True)
    account_number : Mapped[str] = mapped_column(String(500), nullable=True)
    collateral_value : Mapped[float] = mapped_column(Float, nullable=True)
    prepayment_penalty : Mapped[float] = mapped_column(Float, nullable=True)
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="loans")

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "loan_id": self.loan_id,
            "lender": self.lender,
            "loan_type": self.loan_type,
            "original_amount": self.original_amount,
            "current_balance": self.current_balance,
            "interest_rate": self.interest_rate,
            "tenure_months": self.tenure_months,
            "emi_amount": self.emi_amount,
            "status": self.status,
            "open_date": self.open_date,
            "due_date": self.due_date,
            "account_number": self.account_number,
            "collateral_value": self.collateral_value,
            "prepayment_penalty": self.prepayment_penalty,
        }