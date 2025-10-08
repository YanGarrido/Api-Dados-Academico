from pydantic import BaseModel, ConfigDict

class CurriculumInfo(BaseModel):
    periodo: int
    codcurso: str
    coddisc: str
    codgrade: str | None = None
    descricao: str | None = None

    model_config = ConfigDict(from_attributes=True)