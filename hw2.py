from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
        
user_list: list[User] = []

@app.get("/users")
async def get_users():
    return {"users": user_list}

@app.post("/users")
async def add_user(user: User):
    user_list.append(user)
    return {"users": user_list}

@app.delete("/users")
async def delete_user(index: int = 0):
    user_list.pop(index)
    return {"users": user_list}



class Employer(BaseModel):
    employer_name: str
    username: str
        
employer_list: list[Employer] = []

@app.get("/employers")
async def get_employers():
    return {"employers": employer_list}

@app.post("/employers")
async def add_employer(employer: Employer):
    employer_list.append(employer)
    return {"employers": employer_list}

@app.delete("/employers")
async def delete_employer(index: int = 0):
    employer_list.pop(index)
    return {"employers": employer_list}



class JobListing(BaseModel):
    title: str
    location: str
    type: str
    experience: str
    salary: str
        
listing_list: list[JobListing] = []

@app.get("/listings")
async def get_listings():
    return {"listings": listing_list}

@app.post("/listings")
async def add_listing(listing: JobListing):
    listing_list.append(listing)
    return {"listings": listing_list}

@app.delete("/listings")
async def delete_listing(index: int = 0):
    listing_list.pop(index)
    return {"listings": listing_list}