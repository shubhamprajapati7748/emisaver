from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class SwitchRequest(Base):
    __tablename__ = "switch_requests"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    from_loan_id : Mapped[str] = mapped_column(String(500), nullable=True)
    to_lender : Mapped[str] = mapped_column(String(500), nullable=True)
    status : Mapped[str] = mapped_column(String(500), nullable=True)