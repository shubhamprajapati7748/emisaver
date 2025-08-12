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
    tenure_upto : Mapped[int] = mapped_column(Integer, nullable=True)
    loan_tags : Mapped[list[str]] = mapped_column(JSON, nullable=True)
    status : Mapped[bool] = mapped_column(Boolean, nullable=True)
    processing_fee : Mapped[float] = mapped_column(Float, nullable=True)
    prepayment_penalty : Mapped[float] = mapped_column(Float, nullable=True)
    offer_valid_till : Mapped[str] = mapped_column(String(500), nullable=True)
    eligibility_criteria : Mapped[str] = mapped_column(String(500), nullable=True)
    terms_and_conditions : Mapped[str] = mapped_column(String(500), nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "lender_name": self.lender_name,
            "loan_type": self.loan_type,
            "roi_start": self.roi_start,
            "roi_end": self.roi_end,
            "min_loan_amount": self.min_loan_amount,
            "max_loan_amount": self.max_loan_amount,
            "tenure_upto": self.tenure_upto,
            "loan_tags": self.loan_tags,
            "status": self.status,
            "processing_fee": self.processing_fee,
            "prepayment_penalty": self.prepayment_penalty,
            "offer_valid_till": self.offer_valid_till,
            "eligibility_criteria": self.eligibility_criteria,
            "terms_and_conditions": self.terms_and_conditions
        }