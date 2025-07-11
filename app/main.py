# app/adk/main.py - Updated with minor fixes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
# from app.database.session import AsyncSessionLocal
# from app.database.init_db import init_db
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from app.api.v1.endpoints import (health, users)
from app.mcp.fi_mcp import FiMCP


# Application state management 
class ApplicationState:
    def __init__(self):
        self.fi_mcp = None
    
    async def initialize(self):
        self.fi_mcp = FiMCP()

    async def shutdown(self):
        self.fi_mcp = None

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs",
    description="EMISaver AI - Google ADK v1.0.0 Implementation",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    app.state.app_state = ApplicationState()
    await app.state.app_state.initialize()
    # configure_opik()
    
@app.on_event("shutdown")
async def shutdown_event():
    await app.state.app_state.shutdown()
    
app.state.app_state = ApplicationState()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def show_docs_reference() -> HTMLResponse:
    """Root endpoint to display the API documentation.

    Returns:
    -------
        HTMLResponse: The HTML content to display the API documentation.

    """
    html_content = """
<!DOCTYPE html>
<html>
    <head>
        <title>EMISaver API</title>
    </head>
    <body>
        <h1>Welcome to the EMISaver API</h1>
        <p>Please visit the <a href="http://127.0.0.1:8000/docs">docs</a> for more information.</p>
    </body>
</html>
    """
    return HTMLResponse(content=html_content)

app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# fi_mcp = FiMCP()

# @app.get("/")
# async def root():
#     return {"message": "EMISaver AI - Google ADK v1.0.0 Implementation"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "service": "emisaver-ai-adk", "version": "2.0.0"}

# @app.post("/sign-up")
# async def sign_up():
#     return {"status": "success", "message": "User signed up successfully"}

# @app.post("/get-user-info")
# async def get_user_info():
#     try:
#         user_info : UserInfo = await fi_mcp.get_response(FETCH_USER_DETAILS_SYSTEM_PROMPT)
#         # save these details in the database
        
#         return {"status": "success", "message": user_info}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
