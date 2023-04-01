from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
     title:str
     content:str
     published: bool=True    #default value "True"
class PostCreate(PostBase):
     pass

class Post(BaseModel):
     id: int
     title:str
     content:str
     published:bool
     created_at : datetime

                                                 #pydantic model only works with dictionary 
     class Config:                               #class is used to convert the response into dictionary
          orm_mode =True