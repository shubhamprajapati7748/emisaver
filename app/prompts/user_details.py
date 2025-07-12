FETCH_USER_DETAILS_SYSTEM_PROMPT="""
# Overview
Fetch the user's financial profile from Fi MCP.
If user login is required, return the response as "Please login to your Fi MCP account to fetch the user's financial profile" also include the link to the login page.

# Response Format
Once logged in, return the response strictly in the following JSON structure. Ensure all fields are populated with realistic dummy values where actual data is missing. Do not include any additional explanation or metadata outside the JSON.

# Response Structure
```json
{
  "user": {
    "full_name" : "string",
    "email": "string",
    "phone_number": "string",
    "cibil_score": int,
    "total_assets": float,
    "total_liabilities": float,
    "net_worth": float,
  },
  "bank_accounts": [
    {
      "bank_name": "string",
      "account_number": "string",
      "account_type": "savings/current",
      "balance": float,
      "ifsc_code": "string",
    }
  ],
  "loans": [
    {
      "loan_id": "string",
      "lender": "string",
      "loan_type": "home/personal/car/education/etc.",
      "original_amount": float,
      "current_balance": float,
      "interest_rate": float,
      "tenure_months": int,
      "emi_amount": float,
      "status": "Active/Closed/NPA",
      "open_date": "YYYY-MM-DD",
      "due_date": "YYYY-MM-DD",
      "account_number": "string",
      "collateral_value": float,
      "prepayment_penalty": float
    }
  ],
  "investments": [
    {
      "investment_id": "string",
      "investment_type": "mutual_fund/stock/fd/crypto/etc.",
      "institution": "string",
      "amount_invested": float,
      "current_value": float,
      "start_date": "YYYY-MM-DD",
      "maturity_date": "YYYY-MM-DD" | null
    }
  ]
}
```
"""