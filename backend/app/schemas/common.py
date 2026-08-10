from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

class ErrorResponse(BaseModel):
    detail: str

class SuccessResponse(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
