from fastapi import FastAPI

app = FastAPI() # Create an object of FastAPI Class

@app.get("/") # get request -> at url "/" 
def sayHello():
    return {"message":"Hello Buddy"}

@app.get("/about")
def aboutus():
    return {"message":"FastAPI"}