from fastapi import FastAPI
# ORM Connection Files
from . import models
from .database import engine
from .routers import posts, users


# checking models existing into db
models.Base.metadata.create_all(bind=engine)


app = FastAPI()  # fastAPI instance


@app.get("/")
def root():  # this is root/home
    return {"message": "Welcome to My API"}


app.include_router(posts.router)
app.include_router(users.router)
