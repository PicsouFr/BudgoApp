from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterOut(BaseModel):
    ok: bool