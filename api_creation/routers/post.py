

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
import models
import schemas
from database import get_db
import oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()   # this code refers to display the posts which was created by the logined in user.
    return posts
 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post_id(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post

   


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:                  # This condition is used to whether the user got authorized or not, if not will raise exception.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}",response_model=schemas.Post)
# def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#     #                (post.title, post.content, post.published, str(id)))

#     # updated_post = cursor.fetchone()
#     # conn.commit()

#     post = db.query(models.Post).filter(models.Post.id == id)
#     post_query = post.first()

#     if post_query == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
    
#     # posts = post()
#     print(post_query.title)

    
#     post_query.update(updated_post.dict(),synchronize_session=False)
#     db.commit()

#     return post_query

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post_query.owner_id != current_user.id:                  # This condition is used to whether the user got authorized or not, if not will raise exception.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")


    post_query.title = updated_post.title
    post_query.content = updated_post.content
    # post_query.published = updated_post.published 
    db.commit()

    
    # post_query.update(updated_post.dict(),synchronize_session=False)

    # db.commit()

    return post_query
    # post_query = db.query(models.Post).filter(models.Post.id == id)
    # post = post_query.first()
    # if post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exists")
    # post_query.update(updated_post.dict(),synchronize_session=False)
    # db.commit()
    # return {"data":post_query.first()}
    