from pydantic import BaseModel, ConfigDict

class ProfessorInfo(BaseModel):
    code: str | None = None
    name: str | None = None
    email: str | None = None
    
    model_config = ConfigDict(from_attributes=True)