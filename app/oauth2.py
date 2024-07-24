from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


conn,cursor = database.establish_connection()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extracting user_id and converting it to string
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        # Convert user_id to string if it's not None
        user_id_str = str(user_id)
        token_data = schemas.TokenData(id=user_id_str)
    except JWTError:
        raise credentials_exception
    return token_data




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token,credentials_exception)
