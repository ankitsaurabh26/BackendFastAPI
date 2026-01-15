# You can do validation on data from multiple fields using Model Validator. 
# 
# Say you will only create an object for the Patient age > 60 if they have an emergency_contact in their contact field. Here two fields are involved in validation right? age and contact 

from pydantic import BaseModel, model_validator, EmailStr
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(self):
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError("Patients older than 60 must have an emergency contact!")
        return self

# Sample data
patient_info = {
    'name': 'Laalu',
    'age': 69,
    'weight': 89.4,
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

insert_data_patient(patient_1)