from typing import Optional

from pydantic import BaseModel


class EmailBody(BaseModel):
    name: str
    phone: Optional[str] = None
    email: str
    message: str
