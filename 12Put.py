from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)

class Patient(BaseModel):
    # {"P001": {"name": "Ananya Verma", "city": "Guwahati", "age": 28, "gender": "female", "height": 1.65, "weight": 90.0, "bmi": 33.06, "verdict": "Obese"}
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P003'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City in which the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['Male','Female','Others'], Field(..., description="Gender of the pateint", examples=["Male","Female","Others"])]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meter")]
    weight: Annotated[float, Field(..., gt=0, description=("Weight of the patient in Kg"))]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi<18.5:
            return "Under-Weight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Over-Weight"
        else:
            return "Obese"
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(gt=0, lt=120, default=None)]
    gender: Annotated[Optional[Literal['Male','Female','Others']], Field(default=None)]
    height: Annotated[Optional[float], Field(gt=0, default=None)]
    weight: Annotated[Optional[float], Field(gt=0,default=None)]

@app.post('/create')
def create_patient(patientdata:Patient):
    # load existing data
    data = load_data()

    # check if the patient is already existing
    if patientdata.id in data:
        raise HTTPException (status_code=400, detail="Patient already exist")

    # add new patient to the database
    # note: patientdata is a pydantic object whereas data is dictionary
    data[patientdata.id] = patientdata.model_dump(exclude=['id'])

    # save into the json file
    save_data(data) # call the function created above

    return JSONResponse(status_code=201, content={"message":"Patient created successfully!"})

@app.put('/edit/{patient_id}')
def updatePatient(patient_id: str, update_patient:PatientUpdate):
    data = load_data()

    # if the patient id is in database
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found :(")
    
    existing_patient_info = data[patient_id]

    # convert update_patient (Pydantic object) to dictionary
    updated_patient_info = update_patient.model_dump(exclude_unset=True)
    # exclude_unset = True: only include the fields that you actually sent in your request, skipping any fields that are just using their default values.

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    # now there is an issue as we feed new data, there might be change in the verdict and bmi based on the calculation

    # What is the solution then?
    # existing_patient_info -> Pydantic object -> Updated BMI + Verdict -> Pydantic Object -> Dictionary

    # existing_patient_info -> Pydantic object -> Updated BMI + Verdict
    existing_patient_info['id'] = patient_id 
    patient_pydantic_object = Patient(**existing_patient_info)

    # Pydantic Object -> Dictionary
    existing_patient_info = patient_pydantic_object.model_dump(exclude=['id'])

    # add this dict to the data
    data[patient_id] = existing_patient_info

    # save the data
    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Patient Updated"})