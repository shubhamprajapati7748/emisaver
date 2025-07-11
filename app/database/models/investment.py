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
    amount_invested : Mapped[int] = mapped_column(Integer, nullable=True)
    current_value : Mapped[int] = mapped_column(Integer, nullable=True)
    start_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    maturity_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="investments")
