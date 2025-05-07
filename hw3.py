from typing import Optional, List
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
import httpx

sqlite_file_name = "jobs.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)





class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str

class Employer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employer_name: str
    username: str

class JobListing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    location: str
    type: str
    experience: str
    salary: str



@app.post("/users", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user); session.commit(); session.refresh(user)
    return user

@app.get("/users", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    session.delete(user); session.commit()
    return {"ok": True}


@app.post("/employers", response_model=Employer)
def create_employer(employer: Employer, session: Session = Depends(get_session)):
    session.add(employer); session.commit(); session.refresh(employer)
    return employer

@app.get("/employers", response_model=List[Employer])
def read_employers(session: Session = Depends(get_session)):
    return session.exec(select(Employer)).all()

@app.delete("/employers/{employer_id}")
def delete_employer(employer_id: int, session: Session = Depends(get_session)):
    emp = session.get(Employer, employer_id)
    if not emp:
        raise HTTPException(404, "Employer not found")
    session.delete(emp); session.commit()
    return {"ok": True}


@app.post("/listings", response_model=JobListing)
def create_listing(listing: JobListing, session: Session = Depends(get_session)):
    session.add(listing); session.commit(); session.refresh(listing)
    return listing

@app.get("/listings", response_model=List[JobListing])
def read_listings(session: Session = Depends(get_session)):
    return session.exec(select(JobListing)).all()

@app.delete("/listings/{listing_id}")
def delete_listing(listing_id: int, session: Session = Depends(get_session)):
    lst = session.get(JobListing, listing_id)
    if not lst:
        raise HTTPException(404, "Listing not found")
    session.delete(lst); session.commit()
    return {"ok": True}

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_methods=["*"],
  allow_headers=["*"],
)


REMOTIVE_ENDPOINT = "https://remotive.io/api/remote-jobs"

@app.get("/listings/{listing_id}/similar")
async def get_similar_jobs(
    listing_id: int,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    listing = session.get(JobListing, listing_id)
    if not listing:
        raise HTTPException(404, "Listing not found")

    async with httpx.AsyncClient(timeout=10) as client:
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
