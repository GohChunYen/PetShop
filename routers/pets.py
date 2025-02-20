from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db.session import SessionLocal
from starlette import status
from models import Pets, Owners
from sqlalchemy import func


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class PetRequest(BaseModel):
    name: str = Field(min_length=3)
    breed: str = Field(min_length=3)
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None
    owner_id: int

# Find pet owner by pet id
@router.get("/pets/{pet_id}/owner", status_code=status.HTTP_200_OK)
async def find_pet_owner_by_id(db: db_dependency, pet_id: int = Path(gt=0)):
    pet_model = db.query(Pets).filter(Pets.id == pet_id).first()
    
    if not pet_model:
        raise HTTPException(status_code=404, detail='Pet not found.')
    
    owner_model = db.query(Owners).filter(Owners.id == pet_model.owner_id).first()
    
    return owner_model

# Find pet owner by pet name
@router.get("/pets/owner", status_code=status.HTTP_200_OK)
async def find_pet_owner_by_name(db: db_dependency, pet_name: str = Query(...)):
    pet_model = db.query(Pets).filter(Pets.name == pet_name).first()
    
    if not pet_model:
        raise HTTPException(status_code=404, detail='Pet not found.')
    
    owner_model = db.query(Owners).filter(Owners.id == pet_model.owner_id).first()
    
    return owner_model

# Find pets by owner id
@router.get("/pets/owner/{owner_id}", status_code=status.HTTP_200_OK)
async def find_pets_by_owner(db: db_dependency, owner_id: int = Path(gt=0)):
    owner_model = db.query(Owners).filter(Owners.id == owner_id).first()
    
    if not owner_model:
        raise HTTPException(status_code=404, detail='Owner not found.')
    
    pet_model = db.query(Pets).filter(Pets.owner_id == owner_id).all()
    
    return pet_model

# Find pets by owner name
@router.get("/pets", status_code=status.HTTP_200_OK)
async def find_pets_by_owner_name(db: db_dependency, owner_name: str = Query(...)):
    
    owner_models = db.query(Owners).filter(func.concat(Owners.first_name, " ", Owners.last_name).ilike(f"%{owner_name}%")).all()
    
    if not owner_models:
        raise HTTPException(status_code=404, detail='Owner not found.')
    
    pets = []
    # Same name for multiple owners
    for owner in owner_models:
        pet_models = db.query(Pets).filter(Pets.owner_id == owner.id).all()
        pets.extend(pet_models)
    
    return pets

# Create new pets for existing owner
@router.post("/pets", status_code=status.HTTP_201_CREATED)
async def create_pet(db: db_dependency, pet_request: PetRequest):

    owner_model = db.query(Owners).filter(Owners.id == pet_request.owner_id).first()
    
    if not owner_model:
        raise HTTPException(status_code=404, detail='Owner not exist.')
    
    pet_model = Pets(**pet_request.model_dump())
    
    db.add(pet_model)
    db.commit()

# Update existing pets for certain owner
@router.put("/pets/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pet(db: db_dependency, pet_request: PetRequest, pet_id: int = Path(gt=0)):
    
    pet_model = db.query(Pets).filter(Pets.id == pet_id, Pets.owner_id == pet_request.owner_id).first()
    
    if not pet_model:
        raise HTTPException(status_code=404, detail='Pet not found.')
    
    pet_model.name = pet_request.name
    pet_model.breed = pet_request.breed
    pet_model.date_modified = datetime.utcnow()
    
    db.add(pet_model)
    db.commit()


# Delete existing pets from existing owner
@router.delete("/pets/{pet_id}/owner/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(db: db_dependency, pet_id: int = Path(gt=0), owner_id: int = Path(gt=0)):
    pet_model = db.query(Pets).filter(Pets.id == pet_id, Pets.owner_id == owner_id).first()
    
    if not pet_model:
        raise HTTPException(status_code=404, detail='Pet not found.')
    
    db.delete(pet_model)
    db.commit()


