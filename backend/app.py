from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields  
from config import DevConfig
from models import Person, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

migrate = Migrate(app,db) 


api=Api(app,doc='/docs')

#model (serializer)
person_model=api.model(
    "Person",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String(),
    }
)


signup_model=api.model(
    'SignUp',
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String(),
    }
)



@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return{"message":"Hello World"}
    
    
@api.route('/signup')
class SignUp(Resource):
    @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        data=request.get_json()
        
        
        username=data.get('username')
        
        db_user=User.query.filter_by(username=username).first()
        
        if db_user is not None:
            return jsonify({"message":f"User with username{username} already exists"})
        
        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )
        new_user.save()
        
        return new_user,201
        
@api.route('/login')
class Login(Resource):
    def post(self):
        pass
    
    


@api.route('/persons')
class PersonsResource(Resource):
    
    @api.marshal_list_with(person_model)
    def get(self):
            """Get all persons"""
            
            persons=Person.query.all()
            
            
            return persons
    
    
@api.marshal_with(person_model)
@api.expect(person_model)
def post(self):
        """Create a new person"""
        
        data=request.get_json()
        
        new_person=Person(
            title=data.get('title'),
            description=data.get('description'),
        )
        
        new_person.save()
        
        return new_person,201
    
    
    
    
@api.route('/person/<int:id>')
class PersonResource(Resource):
    
    @api.marshal_with(person_model)
    def get(self,id):
        """get a person by id"""
        person=Person.query.get_or_404(id)
        
        return person
    
    
    @api.marshal_with(person_model)
    def put(self,id):
        """update a person by id"""
        
        person_to_update=Person.query.get_or_404(id)
        
        data=request.get_json()
        
        person_to_update.update(data.get('title'),data.get('description'))
        
        return  person_to_update
        
    @api.marshal_with(person_model)
    def delete(self,id): 
        """delete a person by id"""
        
        person_to_delete=Person.query.get_or_404(id)
        
        person_to_delete.delete()
        
        return person_to_delete
        



@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Person":Person
    }
    
    

    
if __name__ =='__main__':
        app.run()