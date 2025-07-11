FETCH_USER_DETAILS_SYSTEM_PROMPT="""
Fetch the user's financial profile from Fi MCP and return the response strictly in the following JSON structure. Ensure all fields are populated with realistic dummy values where actual data is missing. Do not include any additional explanation or metadata outside the JSON.

Return in this format only:
json
```
{
  "user": {
    "full_name" : "string",
    "email": "string",
    "phone_number": "string",
    "cibil_score": 750,
    "total_assets": 1000000,
    "total_liabilities": 450000,
    "net_worth": 550000,
  },
  "bank_accounts": [
    {
      "bank_name": "string",
      "account_number": "string",
      "account_type": "savings/current",
      "balance": 50000,
      "ifsc_code": "string",
    }
  ],
  "loans": [
    {
      "loan_id": "string",
      "lender": "string",
      "loan_type": "home/personal/car/education/etc.",
      "original_amount": 500000,
      "current_balance": 320000,
      "interest_rate": 10.5,
      "tenure_months": 60,
      "emi_amount": 10800,
      "status": "Active/Closed/NPA",
      "open_date": "YYYY-MM-DD",
      "due_date": "YYYY-MM-DD",
      "account_number": "string",
      "collateral_value": 300000,
      "prepayment_penalty": 2.0
    }
  ],
  "investments": [
    {
      "investment_id": "string",
      "investment_type": "mutual_fund/stock/fd/crypto/etc.",
      "institution": "string",
      "amount_invested": 150000,
      "current_value": 170000,
      "start_date": "YYYY-MM-DD",
      "maturity_date": "YYYY-MM-DD"
    }
  ]
}
```
"""