from pydantic import BaseModel, computed_field, EmailStr
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float # kg
    height: float # metre
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/self.height**2, 2)
        return bmi


# Sample data
patient_info = {
    'name': 'Laalu',
    'age': 69,
    'weight': 89.4,
    'height':1.74,
    'married': True, 
    'allergies': ['Pollen', 'Milk'],
    'contact_details': {'phone': '4534565', 'emergency': '467654'}, 
    'email': 'samosemeinaalu@idfc.com'
}

# Create the patient object
patient_1 = Patient(**patient_info)

def insert_data_patient(patient: Patient):
    print(f"Name: {patient.name}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contacts: {patient.contact_details}")
    print(f"BMI: {patient.calculate_bmi}")

insert_data_patient(patient_1)