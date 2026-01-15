from pydantic import BaseModel

# STEP: 01 Define a Pydantic Model (Class)
class Patient(BaseModel):
    name:str
    age:int

patient_info = {'name':'Ambuj','age':35}
# patient_info = {'name':'Ambuj','age':'Thirty'} # This will throw ValidationError as age is not int

# STEP: 02 Instantiate the model with raw input data
patient_1 = Patient(**patient_info)
# Create a starting object first (cannot be empty), another way of validation
# updata = Patient(name="AnyNameForValidation", age=0) 

# STEP: 03 Pass the validated model object
def insert_patient_data(p:Patient): # p is that object (say patient_1 of type Patient)
    print(f"Name inserted: {p.name}")
    print(f"Age inserted: {p.age}")
    print("--- Insertion Done ---")

insert_patient_data(patient_1)

# Let's create some other function
def update_patient_data(upatient: Patient, new_name: str, new_age: int):
    tmp_name = upatient.name
    tmp_age = upatient.age
    upatient.name = new_name
    upatient.age = new_age
    print('--- Updating... ---')
    print(f"Updated Name {tmp_name} to {upatient.name}")
    print(f"Updated Age {tmp_age} to {upatient.age}")

# Now update it as validation of patient_1 has already been done above -> patient_1 = Patient(**patient_info) ; no need to do something like patient_1 = Patient(name="AnyNameForValidation", age=0) again

print(f"Old = {patient_1.name}, {patient_1.age}")

update_patient_data(patient_1,'Mark', 45)
# update_patient_data(patient_1,'Mark', '45') # If I put 45 as string by mistake as well, Pydantic will auto convert the data type to int and things will work here

print(f"New = {patient_1.name}, {patient_1.age}")