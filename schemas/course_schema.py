from typing import List
from pydantic import BaseModel, ConfigDict, Field

class CourseInfo(BaseModel):
    codcurso: int
    name: str | None = None
    turno_id: int
    complemento: str | None = None


    model_config = ConfigDict(from_attributes=True)

class BaseSubject(BaseModel):
    coddisc: str
    name: str

class CourseWithSubjects(CourseInfo):
   subjects: List[BaseSubject] = []

class HasTurmaOut(BaseModel):
    tem_turma: bool
    quant_alunos: int