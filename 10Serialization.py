from pydantic import BaseModel

class Address(BaseModel):
    city:'str'
    state:'str'
    pin:'int'


class Patient(BaseModel):
    name:'str'
    gender:'str'
    age:'int'
    address: Address

address_dict = {'city':'BLR','state':'Karnataka','pin':560037}

address1 = Address(**address_dict)

patient_dict = {
    'name':'Saurabh',
    'gender':'Male',
    'age': 23,
    'address':address1
}
patient1 = Patient(**patient_dict)

tmp = patient1.model_dump()
print(tmp)
print(type(tmp))

tmp_include = patient1.model_dump(include=['name','gender']) # there is "exclude" as well, check exclude_unset on your own!
print(tmp_include)

tmp_json = patient1.model_dump_json()
print(tmp_json)
print(type(tmp_json))