from pydantic import BaseModel, ConfigDict


class SubjectInfo(BaseModel):
    disciplina_id: str
    name: str | None = None
    ch: int | None = None
    chestagio: int | None = None
    chteorica: int | None = None
    chpratica: int | None = None
    chextensao: int | None = None
    chlaboratorial: int | None = None

    model_config = ConfigDict(from_attributes=True)