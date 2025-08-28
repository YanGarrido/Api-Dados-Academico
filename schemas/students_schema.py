from pydantic import BaseModel, ConfigDict

class StudentInfo(BaseModel):
    ra: str | None = None
    name: str | None = None
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)                                            