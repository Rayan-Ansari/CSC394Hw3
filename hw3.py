from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()



class User(BaseModel):
    first_name: str
    last_name: str
    username: str

user_list: list[User] = []

class Employer(BaseModel):
    employer_name: str
    username: str

employer_list: list[Employer] = []

class JobListing(BaseModel):
    title: str
    location: str
    type: str
    experience: str
    salary: str

listing_list: list[JobListing] = []



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




REMOTIVE_ENDPOINT = "https://remotive.com/api/remote-jobs"

@app.get("/listings/{index}/similar")
async def get_similar_jobs(index: int, limit: int = 5):
    try:
        listing = listing_list[index]
    except IndexError:
        raise HTTPException(status_code=404, detail="Listing not found")

    async with httpx.AsyncClient(timeout=10) as client:
        # only title, no location
        params = {"search": listing.title, "limit": limit}
        resp = await client.get(REMOTIVE_ENDPOINT, params=params)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])[:limit]

    return {
        "local_listing": listing,
        "remote_matches": [
            {
                "title": j["title"],
                "company": j["company_name"],
                "url": j["url"],
                "publication_date": j["publication_date"],
                "salary": j.get("salary"),
            }
            for j in jobs
        ],
    }