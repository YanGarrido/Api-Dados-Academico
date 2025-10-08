from typing import List
from pydantic import BaseModel, ConfigDict, Field

class StudentInfo(BaseModel):
    ra: str | None = None
    nome: str | None = None
    emailpessoal: str | None = None
    email: str | None = None
    telefone: str | None = None
    cpf: str | None = None

    model_config = ConfigDict(from_attributes=True)                                            

class CourseInfo(BaseModel):
    codcurso: int
    nome: str | None = None
    codturno: int

class StudentWithCourses(StudentInfo):
   courses: List[CourseInfo] = []