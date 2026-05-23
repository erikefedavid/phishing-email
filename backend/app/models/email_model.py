from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    subject: str = Field("", max_length=500)
    body: str = Field(..., min_length=1)
    headers: str | None = Field(None, max_length=5000)
