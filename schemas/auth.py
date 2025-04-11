from pydantic import BaseModel, validator

class LoginSchema(BaseModel):
    username: str
    password: str

    @validator('password', pre=True)
    def convert_password_to_str(cls, v):
        return str(v)

class RegistrationSchema(BaseModel):
    username: str
    password: str
    email: str
    name: str

    @validator('password', pre=True)
    def convert_password_to_str(cls, v):
        return str(v)

class TokenResponseSchema(BaseModel):
    access_token: str

class ErrorSchema(BaseModel):
    error: str

class ResetPasswordSchema(BaseModel):
    email: str

class ConfirmSignUpSchema(BaseModel):
    username: str
    confirmation_code: str
    session: str = None  # Opcional

    @validator('confirmation_code', pre=True)
    def convert_to_str(cls, v):
        return str(v)
    
class ProtectedInputSchema(BaseModel):
    token: str

class RefreshSchema(BaseModel):
    username: str
    refreshToken: str
