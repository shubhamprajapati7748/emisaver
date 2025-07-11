from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.database.models.user import User

class SwitchRequest(Base):
    __tablename__ = "switch_requests"

    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    from_loan_id : Mapped[str] = mapped_column(String(500), nullable=True)
    to_lender : Mapped[str] = mapped_column(String(500), nullable=True)
    status : Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="switch_requests")