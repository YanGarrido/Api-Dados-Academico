from pydantic import BaseModel, ConfigDict

class CourseInfo(BaseModel):
    id: int
    name: str | None = None
    turno_id: int

    model_config = ConfigDict(from_attributes=True)