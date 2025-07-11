from sqlalchemy import Integer, String, ForeignKey, UUID
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
    balance : Mapped[int] = mapped_column(Integer, nullable=True)
    ifsc_code : Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="bank_accounts")