from pydantic import BaseModel, Field
from uuid import UUID

class User(BaseModel):
    id: str = Field(default="", description="Unique identifier for the user")
    full_name: str = Field(default="", description="Full name of the user")
    email: str = Field(default="", description="Email of the user")
    country_code: str = Field(default="+91", description="Country code of the user")
    phone_number: str = Field(default="", description="Phone number of the user")
    dob: str = Field(default="", description="Date of birth of the user")
    pin_code: str = Field(default="", description="Pin code of the user")
    cibil_score: int = Field(default=0, description="Cibil score of the user")     
    total_assets: float = Field(default=0, description="Total assets of the user")
    total_liabilities: float = Field(default=0, description="Total liabilities of the user")
    net_worth: float = Field(default=0, description="Net worth of the user")

class BankAccount(BaseModel):
    id: str = Field(default="", description="Unique identifier for the bank account")
    bank_name: str = Field(default="", description="Name of the bank")
    account_number: str = Field(default="", description="Account number of the user")
    account_type: str = Field(default="", description="Type of the account")
    balance: float = Field(default=0, description="Balance of the account")
    ifsc_code: str = Field(default="", description="IFSC code of the bank")

class Loan(BaseModel):
    id: str = Field(default="", description="Unique identifier for the loan")
    loan_id: str = Field(default="", description="ID of the loan")
    lender: str = Field(default="", description="Name of the lender")
    loan_type: str = Field(default="", description="Type of the loan")
    original_amount: float = Field(default=0, description="Original amount of the loan")
    current_balance: float = Field(default=0, description="Current balance of the loan")
    interest_rate: float = Field(default=0, description="Interest rate of the loan")
    tenure_months: int = Field(default=0, description="Tenure of the loan in months")
    emi_amount: float = Field(default=0, description="EMI amount of the loan")
    status: str = Field(default="", description="Status of the loan")
    open_date: str = Field(default="", description="Open date of the loan")
    due_date: str = Field(default="", description="Due date of the loan")
    account_number: str = Field(default="", description="Account number of the loan")
    collateral_value: float = Field(default=0, description="Collateral value of the loan")
    prepayment_penalty: float = Field(default=0, description="Prepayment penalty of the loan")

class Investment(BaseModel):
    id: str = Field(default="", description="Unique identifier for the investment")
    investment_id: str = Field(default="", description="ID of the investment")
    investment_type: str = Field(default="", description="Type of the investment")
    institution: str = Field(default="", description="Name of the institution")
    amount_invested: float = Field(default=0, description="Amount invested in the investment")
    current_value: float = Field(default=0, description="Current value of the investment")
    start_date: str = Field(default="", description="Start date of the investment")
    maturity_date: str = Field(default="", description="Maturity date of the investment")
    
class UserInfo(BaseModel):
    user: User = Field(default=None, description="User details")
    bank_accounts: list[BankAccount] = Field(default=[], description="Bank accounts of the user")
    loans: list[Loan] = Field(default=[], description="Loans of the user")
    investments: list[Investment] = Field(default=[], description="Investments of the user")