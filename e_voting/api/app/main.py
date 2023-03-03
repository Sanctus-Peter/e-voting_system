from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import official, auth, user, candidate, vote, view, election

# from . import models
# from .database import engine
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(view.router)
app.include_router(official.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(candidate.candidate_router)
app.include_router(vote.votes_router)
app.include_router(election.router)


app.get("/")


async def root():
    return {"message": "Welcome to our e_voting system"}
