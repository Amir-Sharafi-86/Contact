from pydantic import BaseModel, Field, EmailStr

class ContactSchema(BaseModel):
    name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr
    phone_number: str = Field(...)
    description: str = Field(...)