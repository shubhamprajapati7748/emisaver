from google.adk.agents import LlmAgent, BaseAgent
from app.adk.instructions import SAHI_LOAN_AGENT_INSTRUCTIONS, APPLY_FOR_NEW_LOAN_AGENT_INSTRUCTIONS, APPLY_FOR_REFINANCE_AGENT_INSTRUCTIONS, GENERAL_QUERY_AGENT_INSTRUCTIONS, USER_DETAILS_AGENT_INSTRUCTIONS
from app.adk.tools import get_user_details_tool, get_available_market_loans_tool, save_new_loan_request_tool, save_switch_loan_request_tool, web_search_tool

model = "gemini-2.5-flash"

user_details_agent = LlmAgent(
    name="UserDetailsAgent",
    description="Get the user details and loans from the database.",
    model=model,
    instruction=USER_DETAILS_AGENT_INSTRUCTIONS,
    tools=[get_user_details_tool],
    output_key="user_details",
)

apply_for_new_loan_agent = LlmAgent(
    name="ApplyForNewLoanAgent",
    description="Apply for new loan. Use when user wants to apply for new loan.",
    model=model,
    instruction=APPLY_FOR_NEW_LOAN_AGENT_INSTRUCTIONS,
    tools=[get_available_market_loans_tool, save_new_loan_request_tool],
    output_key="new_loans_output"
)

apply_for_refinance_agent = LlmAgent(
    name="ApplyForRefinanceAgent",
    description="Apply for refinance. Use when user wants to apply for refinance.",
    model=model,
    instruction=APPLY_FOR_REFINANCE_AGENT_INSTRUCTIONS,
    tools=[get_available_market_loans_tool, save_switch_loan_request_tool],
    output_key="refinance_loans_output"
)

general_query_agent = LlmAgent(
    name="GeneralQueryAgent",
    description="GeneralQueryAgent is an expert query agent for providing personalized response to the user query with google search tool if needed.",
    model=model,
    instruction=GENERAL_QUERY_AGENT_INSTRUCTIONS,
    output_key="general_query_output",
    tools=[web_search_tool],
)

sahi_loan_agent = LlmAgent(
    name="SahiLoanAgent",
    description="SahiLoanAgent is orchestrator agent for the loan application process.",
    model=model,
    instruction=SAHI_LOAN_AGENT_INSTRUCTIONS,
    sub_agents=[apply_for_new_loan_agent, apply_for_refinance_agent, general_query_agent, user_details_agent],
    output_key="sahi_loan_agent_output"
)

root_agent = sahi_loan_agent