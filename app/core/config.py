from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Pydantic Settings for the application

    Attributes:
        PROJECT_NAME (str): The name of the project.
        LOCAL_DEVELOPMENT (bool): Whether the application is running in local development mode.
        ENVIROMENT (str): The environment the application is running in.
        APP_VERSION (str): The version of the application.
        DEBUG (bool): Whether the application is running in debug mode.
        HOST (str): The host the application is running on.
        PORT (int): The port the application is running on.
        RELOAD (bool): Whether the application should reload on code changes.
        POSTGRES_HOST (str): The host of the database.
        POSTGRES_PORT (int): The port of the database.
        POSTGRES_USER (str): The user of the database.
        POSTGRES_PASSWORD (str): The password of the database.
        POSTGRES_DB (str): The name of the database.
        MCP_SERVERS_FILE (str): The path to the MCP servers file.
        GEMINI_API_KEY (str): The API key for the Gemini model.
        GEMINI_MODEL (str): The model to use for the Gemini API.
    """

    PROJECT_NAME : str = "EMISaver"
    LOCAL_DEVELOPMENT : bool = True
    ENVIROMENT : str = "local"

    APP_VERSION : str = "0.0.1"
    DEBUG : bool = True 

    # Server settings 
    HOST : str = "0.0.0.0"
    PORT : int = 8000
    RELOAD : bool = True 

    # Postgres Database settings 
    POSTGRES_HOST : str = Field(
        default="localhost",
        description="Database host"
    )
    POSTGRES_PORT : int = Field(
        default=5432,
        description="Database port"
    )
    POSTGRES_USER : str = Field(
        default="postgres",
        description="Database user"
    )
    POSTGRES_PASSWORD : str = Field(
        default="postgres",
        description="Database password"
    )
    POSTGRES_DB : str = Field(
        default="emisaver",
        description="Database name"
    )
    
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """Construct the database URL from individual components."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{str(self.POSTGRES_PORT)}/{self.POSTGRES_DB}"

    # MCP settings 
    MCP_SERVERS_CONFIG_FILE : str = "mcp-servers.json"

    # LLM settings 
    GEMINI_API_KEY : str = Field(
        default=None,
        description="Gemini API key"
    )
    GEMINI_MODEL : str = Field(
        default="models/gemini-2.5-pro",
        description="Gemini model"
    )

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False,
        extra = "ignore"
    )

settings = Settings()