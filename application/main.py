from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user,auth, votes
from fastapi.middleware.cors import CORSMiddleware



# models.Base.metadata.create_all(bind = engine)
#"Look at all my SQLAlchemy models and create the corresponding tables in the database
# if they don't already exist."


app = FastAPI()   #any name can be given

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def home():
    return { "reply" : "hi please login or create id" }