from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse

# import the model 
with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]

# Pydantic model to validate incoming data
class UserInput(BaseModel):
    age:Annotated[int, Field(..., gt=0, lt=120, description="age of the user")]
    weight:Annotated[float, Field(..., gt=0, description="weight of the user in kg")]
    height:Annotated[float, Field(..., gt=0, description="height of the user in meter")]
    income_lpa:Annotated[float, Field(..., gt=0, description="annual salary of the user in LPA")]
    smoker:Annotated[bool, Field(..., description="Is user a smoker")]
    city:Annotated[str, Field(..., description="city the user belongs to")]
    occupation:Annotated[Literal['retired','freelancer','student','government_job','business_owner','unemployed','private_job'], Field(..., description="occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post("/predict")
def predict_premium(userdata: UserInput):
    input_df = pd.DataFrame([
        {
            "bmi":userdata.bmi,
            "age_group":userdata.age_group,
            "lifestyle_risk":userdata.lifestyle_risk,
            "city_tier":userdata.city_tier,
            "income_lpa":userdata.income_lpa,
            "occupation":userdata.occupation
        }
    ])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"predicted_category":prediction})
