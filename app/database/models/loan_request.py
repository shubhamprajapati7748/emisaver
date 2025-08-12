from sqlalchemy import Integer, String, ForeignKey, UUID, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from typing import TYPE_CHECKING
from typing import Dict, Any
import uuid

if TYPE_CHECKING:
    from app.database.models.user import User

class LoanRequest(Base):
    __tablename__ = "loan_requests"
    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    request_type : Mapped[str] = mapped_column(String(500), nullable=False)
    loan_type : Mapped[str] = mapped_column(String(500), nullable=False)
    from_loan_id : Mapped[uuid.UUID] = mapped_column(UUID, nullable=True)
    to_loan_id : Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    status : Mapped[str] = mapped_column(String(500), nullable=False, default="pending")
    
    # Relationship
    user : Mapped["User"] = relationship("User", back_populates="loan_requests")

    def model_dump(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "request_type": self.request_type,
            "loan_type": self.loan_type,
            "from_loan_id": str(self.from_loan_id) if self.from_loan_id else None,
            "to_loan_id": str(self.to_loan_id),
            "status": self.status
        }