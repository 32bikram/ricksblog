from pydantic import BaseModel, EmailStr, conint, Field, ConfigDict
from typing import Optional
from datetime import datetime
from typing import Annotated


class BaseSchema(BaseModel):
    title : str
    content : str
    published : bool

class CreateSchema(BaseSchema):
    pass #inheriting BaseSchema

class ReturnOwner(BaseModel):
    username : str

class Post(BaseModel):
    # id : int
    title: str
    content :  str
    # owner_id : int
    created_at : datetime
    # published : bool
    owner : ReturnOwner    #returns the ReturnOwner class from above we can select what to return from post owner table
    #as owner is a user object so to get username we need a new class
    # we cant just directly write usernmae : str


    class Config:
        from_attributes = True 
        #SQLAlchemy returns a model object, not a dictionary.
        # from_attributes=True tells Pydantic:
        # "If the input is an object, read its attributes
        # (like user.email and user.username) to build this schema."


class GetUser(BaseModel):
    email: EmailStr
    password: str
    username: str

class ReturnUser(BaseModel):
    email: EmailStr
    username: str
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):    #when browser is sending back the access token
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None
    #"id can either be an int or None. If no value is provided, its default value is None."

class vote(BaseModel):
    post_id : int
    dir: Annotated[int, Field(ge=0, le=1)] #direction of vote 0 for dislike, 1 for like 
    Field(
    #ge=0, Greater than or equal to 0
    #le=1 Less than or equal to 1
)

class PostByUserId(BaseModel):
    # id : int
    title: str
    content :  str
    # owner_id : int
    created_at : datetime
    # published : bool
    model_config = ConfigDict(from_attributes=True)

class PostByUserId2(PostByUserId):
    count : int
    username : str

class PostByUserId3(PostByUserId):
    count: int