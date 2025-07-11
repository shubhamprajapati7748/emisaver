from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bank_name : Mapped[str] = mapped_column(String(500), nullable=True)
    account_number : Mapped[str] = mapped_column(String(500), nullable=True)
    account_type : Mapped[str] = mapped_column(String(500), nullable=True)
    balance : Mapped[int] = mapped_column(Integer, nullable=True)
    ifsc_code : Mapped[str] = mapped_column(String(500), nullable=True)