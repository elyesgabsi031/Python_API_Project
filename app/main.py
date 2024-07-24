#importing FastAPI class from fastapi library
from fastapi import FastAPI
from . import database
from .routers import user, recipe,auth




#create an instance of FastAPI class
app = FastAPI()


#path operation(aka route or endpoint)
@app.get("/") #decorator : @ + we reference our fastAPI instance + http method+ ("path") 
def root(): #function
    return {"message": "welcome to my api, check my recipes using route /recipes"}

app.include_router(recipe.router)
app.include_router(user.router)
app.include_router(auth.router)
