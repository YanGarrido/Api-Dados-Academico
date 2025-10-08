from fastapi import FastAPI
from database import engine, Base
from routes import professors_routes, students_routes, course_routes, schedule_routes, curriculum_routes, subjects_routes

from documentacao import api_description, tags_metadata
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API DADOS ACADÊMICOS",
    version="1.0.0",
    description=api_description,
    openapi_tags=tags_metadata
)

app.include_router(professors_routes.router)
app.include_router(students_routes.router)
app.include_router(course_routes.router)
app.include_router(schedule_routes.router)
app.include_router(curriculum_routes.router)
app.include_router(subjects_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar se a API está online.
    """
    return {"status": "ok"}
