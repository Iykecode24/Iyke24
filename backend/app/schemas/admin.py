from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
import uuid

class ApiIntegrationCreate(BaseModel):
    provider: str
    display_name: str
    api_key: str
    endpoint_url: Optional[str] = None

class ApiIntegrationUpdate(BaseModel):
    api_key: Optional[str] = None
    is_active: Optional[bool] = None

class ApiIntegrationResponse(BaseModel):
    id: uuid.UUID
    provider: str
    display_name: str
    is_active: bool
    is_configured: bool
    created_at: datetime

class ModelRegistryCreate(BaseModel):
    name: str
    display_name: str
    type: str
    provider: str
    version: str

class ModelRegistryResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    type: str
    enabled: bool

class GpuInstanceResponse(BaseModel):
    id: uuid.UUID
    provider_instance_id: str
    status: str
    cost_per_hour: float

class SystemStatsResponse(BaseModel):
    total_users: int
    active_projects: int
    running_gpus: int
    monthly_cost_usd: float
