from pydantic import BaseModel, field_validator, Field, EmailStr
from typing import List, Dict
# field_validator validation only works on a single field

class Patient(BaseModel):
    name: str
    age : int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str,str]

    @field_validator('email') # field validation on email - check if the user has hdfc.com or idfc.com in their email or not
    @classmethod # have to add this
    def email_validator(cls, value): # then write the method
        valid_domains = ['hdfc.com','idfc.com']
        # abc@hdfc.com
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    # You can also perform transformation using field_validator
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age',mode='before') # mode = 'before' will give you value before type coerce, suppose you used age = "65" then this field_validator will get 65 as string not as int (which happens after type coerce), by default mode is 'after'
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be between 0 and 100')
    
patient_info = {'name':'Laalu','age':65,'weight': 89.4,'married':True, 'allergies':['Pollen','Milk'],'contact_details':{'phone':'4534565'}, 'email':'samosemeinaalu@idfc.com'}

patient_1 = Patient(**patient_info)

def insert_data_patient(patient:Patient):
    print(patient.name)
    print(patient.allergies)
    print(patient.contact_details)

insert_data_patient(patient_1)