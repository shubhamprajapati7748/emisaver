from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import datetime

class Investment(Base):
    __tablename__ = "investments"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    investment_id : Mapped[str] = mapped_column(String(500), nullable=True)
    investment_type : Mapped[str] = mapped_column(String(500), nullable=True)
    institution : Mapped[str] = mapped_column(String(500), nullable=True)
    amount_invested : Mapped[int] = mapped_column(Integer, nullable=True)
    current_value : Mapped[int] = mapped_column(Integer, nullable=True)
    start_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    maturity_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
