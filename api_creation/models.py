from database import Base
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):                                   #table creation into database
    __tablename__ = "posts"


    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)                      #server_default = 'TRUE' (it set the default value to true)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
                                        
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) #Foreign_key_constraint = users.id , ondelete = "CASCADE" / CASCADE- It is used to delete the posts when user got deleted.
    owner = relationship("User")        #It will returns the owner of the post.
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    

