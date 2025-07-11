import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent
from mcp_use.client import MCPClient
from mcp_use.adapters.langchain_adapter import LangChainAdapter
from langchain_core.output_parsers import JsonOutputParser
from app.schemas.user_details import UserInfo
# from langchain_openai import ChatOpenAI
# from app.core.config import settings
from dotenv import load_dotenv

load_dotenv()

# Create MCPClient from config file
client = MCPClient.from_config_file(
    os.path.join(os.path.dirname(__file__), "mcp-servers.json")
)

# Create LLM
# llm = ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL, api_key=settings.GEMINI_API_KEY)
# llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=os.getenv("ANTHROPIC_API_KEY"))
# llm = ChatOpenAI(model="gpt-4o")
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", api_key=os.getenv("GEMINI_API_KEY"))

# Create agent with the client
# agent = MCPAgent(llm=llm, client=client, max_steps=30)


class FiMCP:
    def __init__(self):
        self.agent = MCPAgent(llm=llm, client=client, max_steps=30)
        self.json_parser = JsonOutputParser(pydantic_object=UserInfo)
    
    async def get_response(self, query: str):
        try:       
            result = await self.agent.run(query)
            parsed_result = self.json_parser.invoke(result)
            return parsed_result
        except Exception as e:
            return "Error: " + str(e)

# fi_mcp = FiMCP()      

# if __name__ == "__main__":
#     response = asyncio.run(fi_mcp.get_response(USER_DETAILS_SYSTEM_PROMPT))
#     print(response)