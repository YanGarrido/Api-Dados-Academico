from typing import List
from pydantic import BaseModel, ConfigDict, Field

class CourseInfo(BaseModel):
    codcurso: int
    nome: str | None = None
    codturno: int
    complemento: str | None = None


    model_config = ConfigDict(from_attributes=True)

class BaseSubject(BaseModel):
    coddisc: str
    nome: str

class ProfessorInfo(BaseModel):
    code: str | None = None
    nome: str | None = None
    cpf: str | None = None
    emailpessoal: str | None = None
    email: str | None = None

class CourseWithSubjects(CourseInfo):
   subjects: List[BaseSubject] = []

class HasTurmaOut(BaseModel):
    tem_turma: bool
    quant_alunos: int

class ClassInfo(BaseModel):
    codcurso: int
    nome: str | None = None
    turno_nome: str
    complemento: str | None = None
    periodo: int
    quant_alunos: int
