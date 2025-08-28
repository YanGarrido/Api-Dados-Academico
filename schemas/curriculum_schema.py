from pydantic import BaseModel, ConfigDict

class CurriculumInfo(BaseModel):
    periodo: int
    curso_id: str
    disciplina_id: str

    model_config = ConfigDict(from_attributes=True)