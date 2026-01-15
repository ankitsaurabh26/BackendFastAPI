from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated
# Annotated and Field together can be used to add metadata

class Patient(BaseModel):
    # name : str = Field(max_length=150)
    name : Annotated[str, Field(max_length=150, title='Name of the patient', description='Give name of the patient in less than 150 characters', examples=['Nitish','Rohan'])] # adding metadata
    # Field also has default = parameter to set a default value

    age : int
    # age : int = Field(gt=0,lt=70)
    # weight : float = Field(gt=0) # here you are ensuring this field does have value greater than 0
    weight: Annotated[float, Field(gt=0, strict=True)] # strict will not allow type coerce i.e, it will not allow '56.2' by default it converts this string to float, right? but with strict = True, it won't do that, it will only work when you strictly give float values nothing else

    married : Optional[bool] = False # this field now becomes optional, you can skip this if want while creating the object; = Default_Value

    # allergies: list # this will be wrong - to achieve this or similar: import List/Dict etc. from typing module
    allergies : List[str] # in here if we just say List (not List[str]) then it means allergies data has to be list that's it -> doing this we are kind of doing two level validation: one allergies has to be a list and second all it's elements should be string
    contact_details: Dict[str, str]

    email: EmailStr
    linkedin_url: AnyUrl # for validating urls

patient_info = {'name':'Laalu','age':65,'weight': 89.4, 'allergies':['Pollen','Milk'],'contact_details':{'phone':'4534565'}, 'email':'samosemeinaalu@laalu.com', 'linkedin_url':'http://linkedin.com/in/laalucmofbihar.com'}

patient_1 = Patient(**patient_info)

def insert_data_patient(patient:Patient):
    print(patient.name)
    print(patient.allergies)
    print(patient.contact_details)
    print(f"Married: {patient.married}")

insert_data_patient(patient_1)