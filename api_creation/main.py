from random import randrange
import time
from typing import Optional
from fastapi import  FastAPI, HTTPException,Response,status,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine,get_db
from routers import post, user ,auth
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)       # this function will create all the models                            


app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fast_api_db',user="postgres",password = "qwerty123",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successfully")
        break
    except Exception as error:
        print("connecting to db failed")
        print("Error: ",error)
        time.sleep(2)




my_posts=[{"title": "title of post 1","content":"content of post 1","id":1},
          {"title": "title of post 2","content":"content of post 1","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


@app.get("/")
def root(): 
    return {"Message":"Hello World"}




    
