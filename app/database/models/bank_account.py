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

    # {'user': {'full_name': 'John Doe', 'email': 'john.doe@example.com', 'phone_number': '+919876543210', 'cibil_score': 807, 'total_assets': 227908, 'total_liabilities': 1195, 'net_worth': 226713}, 
    # 
    # 'bank_accounts': [{'bank_name': 'ICICI Bank', 'account_number': 'XXXXXXXX5479', 'account_type': 'savings', 'balance': 948.04, 'ifsc_code': 'ICIC0006312'}, 
    # 
    # {'bank_name': 'State Bank of India', 'account_number': 'XXXXXXXXXXXXX9754', 'account_type': 'savings', 'balance': 21034.76, 'ifsc_code': 'SBIN0007483'}], 
    # 
    # 'loans': [{'loan_id': 'PVT3090001', 'lender': 'ICICI Bank', 'loan_type': 'Credit Card', 'original_amount': 41229, 'current_balance': 1195, 'interest_rate': 18.0, 'tenure_months': 0, 'emi_amount': 0, 'status': 'Active', 'open_date': '2024-05-22', 'due_date': '2025-05-01', 'account_number': 'PVT3090001', 'collateral_value': 0, 'prepayment_penalty': 0.0}], 'investments': [{'investment_id': '8b5647de-7bd6-4124-b9cf-a19f4ad82114', 'investment_type': 'mutual_fund', 'institution': 'CDSL', 'amount_invested': 85000, 'current_value': 97568.92, 'start_date': '2023-01-15', 'maturity_date': 'N/A'}, {'investment_id': 'a31580d7-2949-461c-a897-3d3dab34b64f', 'investment_type': 'stock', 'institution': 'CDSL', 'amount_invested': 50000, 'current_value': 57537.85, 'start_date': '2022-11-20', 'maturity_date': 'N/A'}]}