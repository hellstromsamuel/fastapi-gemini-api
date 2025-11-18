from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Patient(BaseModel):
    id: int
    name: str
    email: Optional[str] = None


# Simulated in-memory database
patients_db: List[Patient] = []


@app.post("/patients/", response_model=Patient)
def create_patient(patient: Patient):
    for existing_patient in patients_db:
        if existing_patient.id == patient.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    patients_db.append(patient)
    return patient


@app.get("/patients/", response_model=List[Patient])
def get_all_patients():
    return patients_db
