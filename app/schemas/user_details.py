from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    full_name: str = Field(default="", description="Full name of the user")
    email: EmailStr = Field(default="", description="Email of the user")
    phone_number: str = Field(default="", description="Phone number of the user")
    cibil_score: int = Field(default=0, description="Cibil score of the user")     
    total_assets: int = Field(default=0, description="Total assets of the user")
    total_liabilities: int = Field(default=0, description="Total liabilities of the user")
    net_worth: int = Field(default=0, description="Net worth of the user")

class BankAccount(BaseModel):
    bank_name: str = Field(default="", description="Name of the bank")
    account_number: str = Field(default="", description="Account number of the user")
    account_type: str = Field(default="", description="Type of the account")
    balance: int = Field(default=0, description="Balance of the account")
    ifsc_code: str = Field(default="", description="IFSC code of the bank")

class Loan(BaseModel):
    loan_id: str = Field(default="", description="ID of the loan")
    lender: str = Field(default="", description="Name of the lender")
    loan_type: str = Field(default="", description="Type of the loan")
    original_amount: int = Field(default=0, description="Original amount of the loan")
    current_balance: int = Field(default=0, description="Current balance of the loan")
    interest_rate: float = Field(default=0, description="Interest rate of the loan")
    tenure_months: int = Field(default=0, description="Tenure of the loan in months")
    emi_amount: int = Field(default=0, description="EMI amount of the loan")
    status: str = Field(default="", description="Status of the loan")
    open_date: str = Field(default="", description="Open date of the loan")

class Investment(BaseModel):
    investment_id: str = Field(default="", description="ID of the investment")
    investment_type: str = Field(default="", description="Type of the investment")
    institution: str = Field(default="", description="Name of the institution")
    amount_invested: int = Field(default=0, description="Amount invested in the investment")
    current_value: int = Field(default=0, description="Current value of the investment")
    start_date: str = Field(default="", description="Start date of the investment")
    maturity_date: str = Field(default="", description="Maturity date of the investment")
    

class UserInfo(BaseModel):
    user: User = Field(default=None, description="User details")
    bank_accounts: list[BankAccount] = Field(default=[], description="Bank accounts of the user")
    loans: list[Loan] = Field(default=[], description="Loans of the user")
    investments: list[Investment] = Field(default=[], description="Investments of the user")