from sqlalchemy import Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class MarketLoan(Base):
    __tablename__ = "market_loans"

    lender_name : Mapped[str] = mapped_column(String(500), nullable=True)
    loan_type : Mapped[str] = mapped_column(String(500), nullable=True)
    roi_start : Mapped[float] = mapped_column(Float, nullable=True)
    roi_end : Mapped[float] = mapped_column(Float, nullable=True)
    min_loan_amount : Mapped[float] = mapped_column(Float, nullable=True)
    max_loan_amount : Mapped[float] = mapped_column(Float, nullable=True)
    tenure_upto : Mapped[str] = mapped_column(String(500), nullable=True)
    loan_tags : Mapped[list[str]] = mapped_column(JSON, nullable=True)
    status : Mapped[bool] = mapped_column(Boolean, nullable=True)
    eligibility_criteria : Mapped[str] = mapped_column(String(500), nullable=True)
    processing_fee : Mapped[float] = mapped_column(Float, nullable=True)
    prepayment_penalty : Mapped[float] = mapped_column(Float, nullable=True)
    offer_valid_till : Mapped[datetime] = mapped_column(DateTime, nullable=True)