from pydantic import BaseModel, ConfigDict

class ScheduleInfo(BaseModel):
    codturno: int
    horainicial: str | None = None
    horafinal: str | None = None
    
    model_config = ConfigDict(from_attributes=True)