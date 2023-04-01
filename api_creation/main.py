from random import randrange
import time
from typing import Optional
from fastapi import  FastAPI, HTTPException,Response,status,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import models
import schemas
from database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)       # this function will create all the models                            

app = FastAPI()




             

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

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # cursor.fetchall()

    # return {"data":my_posts}
    post = db.query(models.Post).all()
    return{f"data":post }

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published)) 
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data":new_post}
    # print(post.dict())
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}

@app.get("/posts/{id}")
def get_post_id(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts where id = %s """,(str(id),))
    # post = cursor.fetchone()
    post =  db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found") 
    return {"post_detail": post}

@app.delete("/posts/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):

    # cursor.execute(""" delete from posts where id=%s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exists")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" update posts set title=%s,content=%s,published=%s where id= %s returning * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exists")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}
