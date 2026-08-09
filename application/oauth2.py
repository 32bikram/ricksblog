from jose import JWTError, jwt
#pip install python-jose
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from . import schemas, models, database
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login") 
#it tells from the login function we will get the token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy() #we dont wanna change the actual data
    expire = datetime.now(timezone.utc)+timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})    # the key exp here is standard dont change it

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)  #payload,secretke,algo
    return encoded_jwt

def verify_access_token(token : str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        id : str = payload.get("user_id")
        if id is None:
            print("aww jeez")
            raise credential_exception
            print("nooo morty")
        token_data = schemas.TokenData(id = id)
        #creates a pydantic object of TokenData class with the id retrived from payload
    except JWTError:
        raise credential_exception
    
    return token_data

#called from post update, create, delete to get current user
def get_current_user(token : str = Depends(oauth2_schema), db : Session = Depends(database.get_db)):

    credential_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "couldnt validate credentials",
                                         headers = {"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user