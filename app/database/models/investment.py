from sqlalchemy import Integer, String, ForeignKey, Float, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from datetime import datetime   
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.database.models.user import User

class Investment(Base):
    __tablename__ = "investments"

    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    investment_id : Mapped[str] = mapped_column(String(500), nullable=True)
    investment_type : Mapped[str] = mapped_column(String(500), nullable=True)
    institution : Mapped[str] = mapped_column(String(500), nullable=True)
    amount_invested : Mapped[float] = mapped_column(Float, nullable=True)
    current_value : Mapped[float] = mapped_column(Float, nullable=True)
    start_date : Mapped[str] = mapped_column(String(500), nullable=True)
    maturity_date : Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="investments")

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "investment_id": self.investment_id,
            "investment_type": self.investment_type,
            "institution": self.institution,
            "amount_invested": self.amount_invested,
            "current_value": self.current_value,
            "start_date": self.start_date,
            "maturity_date": self.maturity_date
        }