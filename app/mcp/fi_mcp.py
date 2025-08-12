from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent
from mcp_use.client import MCPClient
from langchain_core.output_parsers import JsonOutputParser
from app.schemas.user_details import UserInfo
from app.core.logger import logger
from dotenv import load_dotenv
from app.prompts.user_details import FETCH_USER_DETAILS_SYSTEM_PROMPT
from app.adk.llm import gemini_llm
from app.core.config import settings
from typing import Union
import json
import os

load_dotenv()

# Create MCPClient from config file
client = MCPClient.from_config_file(
    os.path.join(os.path.dirname(__file__), settings.MCP_SERVERS_CONFIG_FILE)
)

class FiMCP:
    def __init__(self):
        self.agent = MCPAgent(llm=gemini_llm, client=client, max_steps=30)
        self.json_parser = JsonOutputParser(pydantic_object=UserInfo)
    
    async def get_response(self, query: str):
        try:       
            return await self.agent.run(query)
        except Exception as e:
            logger.error(f"Error in getting response from Fi MCP: {str(e)}")
            return "Error in getting response from Fi MCP: " + str(e)
    
    async def get_user_info(self) -> Union[UserInfo, str]:
        """Extract and return only the user information from the parsed result"""
        try:
            response = await self.get_response(FETCH_USER_DETAILS_SYSTEM_PROMPT)
            logger.info(f"Raw response from Fi MCP: {response}")
            
            # Check if response is a string (login required or error)
            if isinstance(response, str):
                # Check if it's a login requirement
                if "login" in response.lower() or "please log in" in response.lower():
                    logger.info("Login required response detected")
                    return response
                # Check if it contains JSON data
                elif self._is_json_string(response):
                    logger.info("JSON string response detected, parsing...")
                    # Extract JSON content from code blocks
                    start_idx = response.find('```json') + 7
                    end_idx = response.rfind('```')
                    json_content = response[start_idx:end_idx].strip()
                    parsed_result = self.json_parser.invoke(json_content)
                    logger.info("Successfully parsed JSON response to UserInfo")
                    return parsed_result
                else:
                    logger.info("String response that is not JSON or login requirement")
                    return response
            elif isinstance(response, dict):
                # Response is already a dictionary, convert to UserInfo
                logger.info("Dictionary response detected, converting to UserInfo...")
                try:
                    user_info = UserInfo(**response)
                    logger.info("Successfully converted dictionary to UserInfo")
                    return user_info
                except Exception as e:
                    logger.error(f"Error converting dictionary to UserInfo: {str(e)}")
                    return f"Error converting response to UserInfo: {str(e)}"
            else:
                logger.error(f"Unexpected response type: {type(response)}")
                return f"Unexpected response type: {type(response)}"
                
        except Exception as e:
            logger.error(f"Error in getting user info from Fi MCP: {str(e)}")
            return f"Error in getting user info from Fi MCP: {str(e)}"
        
    def _is_json_string(self, text: str) -> bool:
        """Check if a string contains valid JSON data"""
        text = text.strip()
        
        # Check if it contains JSON code blocks
        if '```json' in text and '```' in text:
            # Extract JSON content from code blocks
            start_idx = text.find('```json') + 7
            end_idx = text.rfind('```')
            if start_idx < end_idx:
                json_content = text[start_idx:end_idx].strip()
                try:
                    json.loads(json_content)
                    return True
                except (json.JSONDecodeError, ValueError):
                    return False
        return False


# fi_mcp = FiMCP()      
# if __name__ == "__main__":
#     response = asyncio.run(fi_mcp.get_response(USER_DETAILS_SYSTEM_PROMPT))
#     print(response)