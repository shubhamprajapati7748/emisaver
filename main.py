

import os 
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from app.adk import root_agent
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import logger
from google.genai import types
from uuid import uuid4
import uvicorn
from dotenv import load_dotenv
from app.adk.tools import get_user_details_tool
from app.database.init_db import init_db
from app.core.config import settings
from google.adk.events import Event, EventActions
import time

load_dotenv()

# Application state management 
class ApplicationState:
    def __init__(self):
        self.db = None
    
    async def initialize(self):
        init_db()

    async def shutdown(self):
        self.db = None

APP_NAME = "sahiloan_agent"
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))


# === SERVICES ===
session_service = InMemorySessionService()

runner = Runner(agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs",
    description="SahiLoan AI - Google ADK v1.0.0 Implementation",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:9002", "http://127.0.0.1:3000", "http://127.0.0.1:9002"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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
        <title>SahiLoan API</title>
    </head>
    <body>
        <h1>Welcome to the SahiLoan API</h1>
        <p>Please visit the <a href="http://127.0.0.1:8080/docs">docs</a> for more information.</p>
    </body>
</html>
    """
    return HTMLResponse(content=html_content)

# === ROUTES ===
@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/initiate-session/{phone_number}")
async def create_session(phone_number: str, background_tasks: BackgroundTasks):
    logger.info(f"Creating session for user: {phone_number}")
    session_id = str(uuid4())

    initial_state = {
        "phone_number": phone_number,
        "user_details": {},
        "loan_requests": [],
    }

    stateful_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=phone_number,
        session_id=session_id,
        state=initial_state,
    )

    response = await get_response(phone_number, session_id, phone_number)
    background_tasks.add_task(update_user_details_background, stateful_session)
    logger.info(f"Session created successfully for user: {phone_number} with session id: {stateful_session.id} !")
    
    return {
        "session_id": stateful_session.id,
        "user_id": stateful_session.user_id,
        "state": stateful_session.state,
        "message": response
    }

@app.get("/users/{phone_number}/sessions/{session_id}/state")
async def get_user_state(phone_number: str, session_id: str):
    try:
        state = await session_service.get_session(app_name=APP_NAME, user_id=phone_number, session_id=session_id)
        return state
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User state not found: {str(e)}")


@app.post("/run")
async def run_agent(payload: dict):
    logger.info("---------------------------------")
    logger.info(f"Running agent with payload: {payload}")
    user_id = payload["user_id"]
    session_id = payload["session_id"]
    message = payload["new_message"]

    response = await get_response(user_id, session_id, message)
    return {
        "response": response
    }


async def get_response(user_id: str, session_id: str, message: str):
    logger.info("Getting response...")
    logger.info(f"Getting response for user: {user_id} with session: {session_id} and message: {message}")
    response = None 
    content = types.Content(
        role='user',
        parts=[types.Part(text=message)]
    )
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response = event.content.parts[0].text
    logger.info(f"LLM Response: {response}")
    return response


async def update_user_details_background(session: Session):
    """Background task to fetch and update user details"""
    try:
        logger.info(f"Getting user details for user: {session.user_id} in background...")
        user_details = get_user_details_tool(session.user_id)
        if user_details is None:
            logger.error(f"User details not found for user: {session.user_id}")
            return

        logger.info(f"User details fetched successfully for user: {user_details} !")
        logger.info(f"Updating user details for user: {session.user_id} in background...")
        current_time = time.time()
        state_changes = {
            "phone_number": session.user_id,
            "user_details": user_details
        }
        actions_with_update = EventActions(state_delta=state_changes)
        system_event = Event(
            invocation_id="inv_user_details_update",
            author="tool",
            actions=actions_with_update,
            timestamp=current_time
        )
        await session_service.append_event(session, system_event)
        logger.info(f"Updated user details for {session.user_id} in background successfully !!!")
    except Exception as e:
        logger.error(f"Error updating user details in background: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)