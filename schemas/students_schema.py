from pydantic import BaseModel, ConfigDict

class StudentInfo(BaseModel):
    ra: str | None = None
    name: str | None = None
    emailpessoal: str | None = None
    email: str | None = None
    telefone: str | None = None
    cpf: str | None = None

    model_config = ConfigDict(from_attributes=True)                                            