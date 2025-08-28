from fastapi import FastAPI
from database import engine, Base
from routes import professors_routes, students_routes, course_routes, schedule_routes, curriculum_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API DADOS ACADÊMICOS",
    version="1.0.0",
    description="Uma API para consultar os dados academicos."
)

app.include_router(professors_routes.router)
app.include_router(students_routes.router)
app.include_router(course_routes.router)
app.include_router(schedule_routes.router)
app.include_router(curriculum_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz para verificar se a API está online.
    """
    return {"status": "ok"}
