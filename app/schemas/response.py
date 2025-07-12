from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any

class BaseResponse(BaseModel):
    status: str = "success | error"
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str | None = None
    data: Any | list[Any] | dict | str | None = None
