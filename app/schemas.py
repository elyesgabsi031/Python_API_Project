from typing import Optional
#we use pydantic to define a schema to control/validate data sent by client and force expected schema
from pydantic import BaseModel, EmailStr

#post request schema// in a post path operation, in the function part, you pass Recipe as argument like this : funct_name(variable: Recipe)
class Recipe(BaseModel):
    name : str
    country:str
    type : str #("Appetizer","Main Course", "Dessert")
    ingredients : str
    instructions : str
    cooking_time : Optional[float] = None
    difficulty: Optional[str] = None

class User(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    email: EmailStr
    id : int

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

