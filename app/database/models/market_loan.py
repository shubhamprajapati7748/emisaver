from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class MarketLoan(Base):
    __tablename__ = "market_loans"

    lender : Mapped[str] = mapped_column(String(500), nullable=True)
    loan_type : Mapped[str] = mapped_column(String(500), nullable=True)
    interest_rate : Mapped[float] = mapped_column(Float, nullable=True)
    max_tenure_months : Mapped[int] = mapped_column(Integer, nullable=True)
    min_loan_amount : Mapped[float] = mapped_column(Float, nullable=True)
    max_loan_amount : Mapped[float] = mapped_column(Float, nullable=True)
    eligibility_criteria : Mapped[str] = mapped_column(String(500), nullable=True)
    processing_fee : Mapped[float] = mapped_column(Float, nullable=True)
    prepayment_penalty : Mapped[float] = mapped_column(Float, nullable=True)
    offer_valid_till : Mapped[datetime] = mapped_column(DateTime, nullable=True)
