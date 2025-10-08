from pydantic import BaseModel, ConfigDict
from schemas.course_schema import CourseInfo

class SubjectInfo(BaseModel):
    coddisc: str
    nome: str | None = None
    ch: int | None = None
    chestagio: int | None = None
    chteorica: int | None = None
    chpratica: int | None = None
    chextensao: int | None = None
    chlaboratorial: int | None = None

    model_config = ConfigDict(from_attributes=True)

class SubjectCompleteInfo(SubjectInfo):
    coddisc: str
    nome: str | None = None
    ch: int | None = None
    chestagio: int | None = None
    chteorica: int | None = None
    chpratica: int | None = None
    chextensao: int | None = None
    chlaboratorial: int | None = None
    cursos: list[CourseInfo] | None = None

    model_config = ConfigDict(from_attributes=True)