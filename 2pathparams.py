from fastapi import FastAPI, Path
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

# Path parameters are used to define dynamic segments of the URL path to identify a specific resource, such as a user ID or product ID

@app.get("/view") 
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
# def view_patient(patient_id : str): # This will work fine as well
def view_patient(patient_id : str = Path(..., description="ID of the patient in the DB", example="P001")): # but to increase clarity we can do this
    # load all the patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    return {"Error":"Patient not found!"}

# The path() function in FastAPI is used to provide metadata, validation rules, and documentation hints for path parameters in API endpoints