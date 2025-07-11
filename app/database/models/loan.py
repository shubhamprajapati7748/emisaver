

from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class Loan(Base):
    __tablename__ = "loans"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    loan_id : Mapped[str] = mapped_column(String(500), nullable=True)
    lender : Mapped[str] = mapped_column(String(500), nullable=True)
    loan_type : Mapped[str] = mapped_column(String(500), nullable=True)
    original_amount : Mapped[int] = mapped_column(Integer, nullable=True)
    current_balance : Mapped[int] = mapped_column(Integer, nullable=True)
    interest_rate : Mapped[float] = mapped_column(Float, nullable=True)
    tenure_months : Mapped[int] = mapped_column(Integer, nullable=True)
    emi_amount : Mapped[int] = mapped_column(Integer, nullable=True)
    status : Mapped[str] = mapped_column(String(500), nullable=True)
    open_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    due_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    account_number : Mapped[str] = mapped_column(String(500), nullable=True)
    collateral_value : Mapped[int] = mapped_column(Integer, nullable=True)
    prepayment_penalty : Mapped[int] = mapped_column(Integer, nullable=True)
