from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.models.bank_account import BankAccount
    from app.database.models.loan import Loan
    from app.database.models.investment import Investment
    from app.database.models.swith_request import SwitchRequest

class User(Base):
    __tablename__ = "users"

    full_name : Mapped[str] = mapped_column(String(500), nullable=True)
    email : Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    phone_number : Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    cibil_score : Mapped[int] = mapped_column(Integer, nullable=True)
    total_assets : Mapped[int] = mapped_column(Integer, nullable=True)
    total_liabilities : Mapped[int] = mapped_column(Integer, nullable=True)
    net_worth : Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    bank_accounts : Mapped[list["BankAccount"]] = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    loans : Mapped[list["Loan"]] = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    investments : Mapped[list["Investment"]] = relationship("Investment", back_populates="user", cascade="all, delete-orphan")
    switch_requests : Mapped[list["SwitchRequest"]] = relationship("SwitchRequest", back_populates="user", cascade="all, delete-orphan")
