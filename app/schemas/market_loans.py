from pydantic import BaseModel, Field

class MarketLoan(BaseModel):
    lender_name: str = Field(default="", description="Name of the lender")
    loan_type: str = Field(default="", description="Type of the loan")
    roi_start: float = Field(default=0, description="Start of the ROI")
    roi_end: float = Field(default=0, description="End of the ROI")
    min_loan_amount: float = Field(default=0, description="Minimum loan amount")
    max_loan_amount: float = Field(default=0, description="Maximum loan amount")
    tenure_upto: int = Field(default=0, description="Tenure upto")
    loan_tags: list[str] = Field(default=[], description="Tags of the loan")
    status: bool = Field(default=False, description="Status of the loan")
    processing_fee: float = Field(default=0, description="Processing fee of the loan")
    prepayment_penalty: float = Field(default=0, description="Prepayment penalty of the loan")
    offer_valid_till: str = Field(default="", description="Offer valid till")
    eligibility_criteria: str = Field(default="", description="Eligibility criteria of the loan")
    terms_and_conditions: str = Field(default="", description="Terms and conditions of the loan")
    