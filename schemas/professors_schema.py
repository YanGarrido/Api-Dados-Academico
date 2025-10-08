from pydantic import BaseModel, ConfigDict

class ProfessorInfo(BaseModel):
    code: str | None = None
    nome: str | None = None
    cpf: str | None = None
    emailpessoal: str | None = None
    email: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class ProfessorWithSubjects(ProfessorInfo):
    subjects: list[dict[str, str]] = []
    
    model_config = ConfigDict(from_attributes=True)