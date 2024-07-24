#importing FastAPI class from fastapi library
from fastapi import HTTPException, status, APIRouter
from .. import schemas, database, utils  #has our pydantic model / db conn / password hash




 
router = APIRouter(
    tags=['Users']
)

#connection to database
conn,cursor = database.establish_connection()




#create a user
@router.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def CreateUser(user : schemas.User):
    hashed_password= utils.hash(user.password)
    user.password = hashed_password
    cursor.execute("""INSERT INTO users(email,password) VALUES(%s,%s) RETURNING *""",(user.email,user.password))
    new_user = cursor.fetchone()
    conn.commit()
    return new_user

#get a user by id
@router.get("/users/{id}",response_model=schemas.UserOut)
def get_user(id: int):
    cursor.execute(""" SELECT * FROM users WHERE id = %s """,(id,))
    get_user = cursor.fetchone()
    
    if get_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"user with id number {id} not found")
    return get_user