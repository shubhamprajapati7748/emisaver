from sqlalchemy import Integer, String, ForeignKey, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.database.models.user import User

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bank_name : Mapped[str] = mapped_column(String(500), nullable=True)
    account_number : Mapped[str] = mapped_column(String(500), nullable=True)
    account_type : Mapped[str] = mapped_column(String(500), nullable=True)
    balance : Mapped[float] = mapped_column(Float, nullable=True)
    ifsc_code : Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="bank_accounts")

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "bank_name": self.bank_name,
            "account_number": self.account_number,
            "account_type": self.account_type,
            "balance": self.balance,
            "ifsc_code": self.ifsc_code
        }