from fastapi import FastAPI
from db.base_class import Base
import models
from db.session import engine
from routers import owners, pets
from config import settings

def create_tables():         
	Base.metadata.create_all(bind=engine)
        
        
def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    create_tables()
    return app

app = start_application()

app.include_router(owners.router)
app.include_router(pets.router)

@app.get("/")
def home():
    return {"msg":"Welcome to PetShop"}