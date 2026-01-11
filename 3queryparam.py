from fastapi import FastAPI, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="sort on the basis of height, weight or BMI"), order: str = Query('asc', description="Sort in ascending or descending order") ): # Query() is similar to Path()
# Remember: Query(...,) means it is a mandatory parameter
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid order select between asc and desc")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data