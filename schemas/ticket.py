from datetime import datetime

from pydantic import BaseModel

class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
