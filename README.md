# EMI Saver

# To run fastapi app

`uvicorn app.main:app --reload`

`python -m app.database.init_db`


# Todo list 

- FiMCP get the - local postgres
    - loan
    - investments 
    - bank account
    - user info 


## Idea 

EMI Saver 

1. Get all user loans -> FiMCP 
2. Real data Market loans availables -> RAG Pipeline
3. Suggest the loan alternatives -> Switch (Save the amount)
4. Recommendation for new loan
5. UI design (Shiva)
    - User onboarding 
        - Phone number (FireAuth)
        - OTP
    - User Dashboard 
        - User data 
        - Loans list 
    - Loans details 
        - Best Alternative 
            - RAG pipelines -> Suggestion 

6. Sandeep (AI-agent) - EMI Comparison Engine: Compares your current loans with market options to find lower interest rates.
    Personalized Refinance Suggestions: Recommends the best refinance deals with clear EMI and interest savings.

    - Suggest the Process of Refinance 
    - Switching guide 

7. Chatbot (enhancements)

## Tech / tools 

- RAG Pipeline
- Loan Agent - ADK
- Vertex AI 
- FireStore - Postgres
- Langchain
