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
        GOOGLE_CLOUD_PROJECT (str): The ID of the Google Cloud Project.
        GOOGLE_CLOUD_LOCATION (str): The location of the Google Cloud Project.
        GOOGLE_CLOUD_STORAGE_BUCKET (str): The bucket name for the Google Cloud Storage.
        GCS_DEFAULT_STORAGE_CLASS (str): The default storage class for the GCS.
        GCS_DEFAULT_LOCATION (str): The default location for the GCS.
        GCS_LIST_BUCKETS_MAX_RESULTS (int): The maximum number of buckets to list.
        GCS_LIST_BLOBS_MAX_RESULTS (int): The maximum number of blobs to list.
        GCS_DEFAULT_CONTENT_TYPE (str): The default content type for the GCS.
        RAG_DEFAULT_EMBEDDING_MODEL (str): The embedding model to use for the RAG.
        RAG_DEFAULT_TOP_K (int): The number of results to return for the RAG.
        RAG_DEFAULT_SEARCH_TOP_K (int): The number of results to return for the RAG search.
        RAG_DEFAULT_VECTOR_DISTANCE_THRESHOLD (float): The threshold for the RAG vector distance.
        RAG_DEFAULT_PAGE_SIZE (int): The page size for the RAG.
    """

    PROJECT_NAME : str = "SahiLoan"
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
        default="localhost", # Replace with your database host
        description="Database host"
    )
    POSTGRES_PORT : int = Field(
        default=5432, # Default port for PostgreSQL
        description="Database port"
    )
    POSTGRES_USER : str = Field(
        default="shubhamp", # Default user for PostgreSQL
        description="Database user"
    )
    POSTGRES_PASSWORD : str = Field(
        default="postgres", # Default password for PostgreSQL
        description="Database password"
    )
    POSTGRES_DB : str = Field(
        default="sahiloan", # Default database name for PostgreSQL
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
        default=None, # Replace with your API key
        description="Gemini API key"
    )
    GEMINI_MODEL : str = Field(
        default="models/gemini-2.5-pro",
        description="Gemini model"
    )

    # Google Cloud Project Settings
    GOOGLE_CLOUD_PROJECT : str = Field(
        default=None, # Replace with your project ID
        description="Google Cloud Project ID"
    )
    GOOGLE_CLOUD_LOCATION : str = Field(
        default="us-central1", # Default location for Vertex AI and GCS resources
        description="Google Cloud Location"
    )

    GOOGLE_CLOUD_STORAGE_BUCKET : str = Field(
        default="gs://sahiloan-staging",
        description="Google Cloud Storage Bucket"
    )

    # GCS Storage Settings
    GCS_DEFAULT_STORAGE_CLASS : str = "STANDARD"
    GCS_DEFAULT_LOCATION : str = "US"
    GCS_LIST_BUCKETS_MAX_RESULTS : int = 50
    GCS_LIST_BLOBS_MAX_RESULTS : int = 100
    GCS_DEFAULT_CONTENT_TYPE : str = "application/json"  # Default content type for uploaded files

    # RAG Corpus Settings
    RAG_DEFAULT_EMBEDDING_MODEL : str = "text-embedding-004"
    RAG_DEFAULT_TOP_K : int = 10  # Default number of results for single corpus query
    RAG_DEFAULT_SEARCH_TOP_K : int = 5  # Default number of results per corpus for search_all
    RAG_DEFAULT_VECTOR_DISTANCE_THRESHOLD : float = 0.5
    RAG_DEFAULT_PAGE_SIZE : int = 50  # Default page size for listing files

    # DATA File paths
    METADATA_FILE_PATH : str = "data/loans_provider.json"

    # Agent Settings
    AGENT_NAME : str = "SahiLoan_agent"   
    AGENT_MODEL : str = "gemini-2.0-flash-exp"
    AGENT_OUTPUT_KEY : str = "last_response"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False,
        extra = "ignore"
    )

settings = Settings()