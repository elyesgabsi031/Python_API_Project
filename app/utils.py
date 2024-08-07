from passlib.context import CryptContext
import logging
logging.getLogger('passlib').setLevel(logging.ERROR) #hides warning caused by new version of bcrypt



#telling passlib what is the default hashing algo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)