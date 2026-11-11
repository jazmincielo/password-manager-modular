from sqlmodel import SQLModel, Field
from typing import Optional

class VaultEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_name: str = Field(index=True)
    username: str
    encrypted_password: str
    notes: Optional[str] = Field(default="")
