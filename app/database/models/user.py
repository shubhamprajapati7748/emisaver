from sqlalchemy import Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.bank_account import BankAccount
    from app.database.models.loan import Loan
    from app.database.models.investment import Investment
    from app.database.models.swith_request import SwitchRequest
    from app.database.models.loan_request import LoanRequest
    
class User(Base):
    __tablename__ = "users"

    full_name : Mapped[str] = mapped_column(String(500), nullable=True)
    email : Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    country_code : Mapped[str] = mapped_column(String(500), nullable=True, default="+91")
    phone_number : Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    dob : Mapped[str] = mapped_column(String(500), nullable=True)
    pin_code : Mapped[str] = mapped_column(String(500), nullable=True)
    cibil_score : Mapped[int] = mapped_column(Integer, nullable=True)
    total_assets : Mapped[float] = mapped_column(Float, nullable=True)
    total_liabilities : Mapped[float] = mapped_column(Float, nullable=True)
    net_worth : Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    bank_accounts : Mapped[list["BankAccount"]] = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    loans : Mapped[list["Loan"]] = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    investments : Mapped[list["Investment"]] = relationship("Investment", back_populates="user", cascade="all, delete-orphan")
    switch_requests : Mapped[list["SwitchRequest"]] = relationship("SwitchRequest", back_populates="user", cascade="all, delete-orphan")
    loan_requests : Mapped[list["LoanRequest"]] = relationship("LoanRequest", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "email": self.email,
            "country_code": self.country_code,
            "phone_number": self.phone_number,
            "dob": self.dob,
            "pin_code": self.pin_code,
            "cibil_score": self.cibil_score,
            "total_assets": self.total_assets,
            "total_liabilities": self.total_liabilities,
            "net_worth": self.net_worth
        }