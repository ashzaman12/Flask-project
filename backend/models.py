import email
from re import U
from turtle import title
from exts import db 


"""
class Person:
    id:int primary key
    title:str
    description:str (text)    
"""

class Person(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(),nullable=False)
    desciption=db.Column(db.Text(),nullable=False)
    
    def __repr__(self):
        return f"<Person {self.title}>"
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self,title,description):
        self.title=title
        self.desciption=description
        
        db.session.commit()
        

#user model for creating 

"""
class User:
    id:int integer
    username:string
    email:string
    password:string
"""

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(10),nullable=False,unique=True)
    email=db.Column(db.String(25),nullable=False,unique=True)
    password=db.Column(db.Text(25),nullable=False)
    
    def __repr__(self):
        return f"<User {self.username}>"