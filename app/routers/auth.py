from fastapi import HTTPException, status, APIRouter,Response,Depends
from .. import database, schemas,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

#connection to database
conn,cursor = database.establish_connection()

@router.post('/login', response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm=Depends()):
    cursor.execute("""SELECT * FROM users WHERE email = %s""",(user_credentials.username,))
    log_user = cursor.fetchone()
    conn.commit()
    if not log_user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password,log_user['password']):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail="Invalid credentials")
    
    
    access_token = oauth2.create_access_token(data={"user_id": log_user['id']})

    return {"access_token": access_token, "token_type": "bearer"}
   