from  fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
import database ,schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

@router.post('/login',response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print(f"User.email : {models.User.email}")
    print(f"user_credentials : {user_credentials.username}")

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #create a token
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    print(f"access_token : {access_token}")
     #return token
    return {"access_token" : access_token,"token_type": "bearer"}
    
 




