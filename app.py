import os
from flask import Flask,render_template,request, jsonify,request, render_template, flash, redirect, url_for
from flask_migrate import Migrate
import pytz
from models import db, User, Petition, PetitionControl, Game
from dotenv import load_dotenv
from functools import wraps
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt_identity, JWTManager, get_current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from datetime import timedelta, datetime
from flask_cors import CORS, cross_origin
from sqlalchemy import event
from pytz import timezone


load_dotenv()

DB_USER= os.getenv("DB_USER")
DB_URL=os.getenv("DB_URL")
DB_SECRET_KEY= os.getenv("FLASK_SECRET_KEY")



app = Flask(__name__)
auth = HTTPBasicAuth()


app.config['SQLALCHEMY_DATABASE_URI']=(DB_URL)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = (DB_SECRET_KEY)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=3000)
db.init_app(app)

jwt = JWTManager(app)
migrate = Migrate(app, db)
CORS(app)


def get_current_time():
   return datetime.now(pytz.timezone('America/Caracas'))

@app.route('/')
def  hello():
    return "HELLO PEOPLE IF YOU ARE HER IS BECAUSE YOU ARE TESTING SOMENTHING"

 
 
@app.route('/form')
def form():
    return render_template('form.html')



def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener el rol del usuario desde la solicitud o la sesión
            user_roles = current_user.roles_user  
            
            # Verificar si el usuario tiene el rol requerido
            if any(role in user_roles for role in roles):
            
            
                return func(*args, **kwargs)
            else:
            
                return jsonify({'error': 'Acceso denegado, verifica si estas ingresnando con un usuario con permisos '}), 403

        return wrapper
    return decorator

 
#CONSULT USER
@app.route('/users', methods=['GET'])
@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@roles_required('calidad','admin')  
def handle_users(user_id = None):
    if request.method == 'GET':
        roles_user=current_user.roles_user
        print("este es el role de", roles_user)
        if user_id is None:
            users = User()
            users = users.query.all()

            return jsonify(list(map(lambda item: item.serialize(), users))) , 200
        else:
            user = User()
            user = user.query.get(user_id)
            if user:
                return jsonify(user.serialize())
        
    return jsonify({"message":" User has not found"}), 404 


#ADD USER

def set_password(password):
    return generate_password_hash(password)

def check_password(hash_password,password):
    return check_password_hash(hash_password,password)

@app.route('/user', methods=['POST'])
@jwt_required()
@roles_required('admin') 
def add_user():
    if request.method == 'POST':
        body = request.json
        print("este es el body ",body)
        user_name = body.get('user_name', None)
        password = body.get('password', None)
        roles_user =body.get('role')
        print("roless", roles_user)

       
        if body is None or user_name is None or password is None or roles_user is None:
            return jsonify ("Por favor verifica que complete todos los campos e intente de nuevo"),404
        else:
            user_exists = User.query.filter_by(user_name=user_name).first()
            if user_exists:
            
             return 'El correo electrónico ya está registrado. Por favor, elige otro.', 426
            
            else:
                password= set_password(password)
                request_user= User(user_name=user_name, password=password, roles_user=roles_user)
                print(request_user)
                db.session.add(request_user)

            try:
                db.session.commit()
                return jsonify("good job bro"), 201
            except Exception as error:
                db.session.rollback(),500
    return jsonify(), 201


#EDIT USER
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id=None):
    if request.method == 'PUT':
        body = request.json
        
        if user_id is None:
            return jsonify({"message":"Bad request"}), 400

        if user_id is not None:
            update_user = User.query.get(user_id)
            if update_user is None:
                return jsonify({"message":"Not found"}), 404
            else:
                update_user.user_name = body["user_name"]
                update_user.password = body["password"]

                try:
                    db.session.commit()
                    return jsonify(update_user.serialize()), 201
                except Exception as error:
                    print(error.args)
                    return jsonify({"message":f"Error {error.args}"}),500

        return jsonify([]), 200
    return jsonify([]), 405

#DELETE USER
@app.route('/users', methods=(['DELETE']))
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if request.method == 'DELETE':
        request.body = request.json

        if user_id is None:
            return jsonify("el usuario no existe"), 400
        
        if user_id is not None:
            delete_user = User.query.get(user_id) 

            if delete_user is None:
                return jsonify({"Message":"Usuario no encontrado"})
            else:
                db.session.delete(delete_user)

                try:
                    db.session.commit()
                    return jsonify("User has been deleted succesfully")
                except Exception as error:
                    print(error.args)
                    db.session.rollback()
                    return jsonify({"message":f"Error {error.args}"}),500

@jwt.user_identity_loader
def user_identity_lookup(user_id):
    return user_id
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        body = request.json
        user_name = body.get('user_name',None)
        password = body.get('password',None)
        roles_user =body.get('role')
        print ("role:", roles_user)

        login_user = User.query.filter_by(user_name=user_name).one_or_none() 
        
        if login_user and check_password_hash(login_user.password,password) == True:
            
            acess_token = create_access_token(identity=login_user.id)
            
            return jsonify({'user_id':login_user.id, 'token':acess_token, "roles_user":login_user.roles_user}),200
        else:
            return jsonify ('acceso denegado, verifica tu usuario y contraseña'),400 

    return jsonify ('bienvenido'),201

@app.route('/logout')
def logout():
    if 'login_user' in db.session:
        db.session.remove('login_user')
    return jsonify("fue un placer")



#CONSULT PETITIONS  

@app.route('/petitions', methods=['GET'])
@app.route('/petitions/<int:petition_id>', methods=['GET'])
@jwt_required()
def handle_petition(petition_id = None):
    if request.method == 'GET':
        
        if petition_id is None:
            petitions = Petition()
            petitions= petitions.query.all()

            return jsonify(list(map(lambda item: item.serialize(), petitions))) , 200
        else:
            petition = Petition()
            petition = petition.query.get(petition_id)
            if petition:
                return jsonify(petition.serialize())
            
        return jsonify({"message":" Petition has not found"}), 404 


#CONSULT PETITION ACTIVE
    
@app.route('/petitions-active', methods=['GET'])
@app.route('/petitions-active/<int:petition_id>', methods=['GET'])
@jwt_required()
def handle_active_petition(petition_id = None):
    if request.method == 'GET':
        
        if petition_id is None:
            active_petitions = Petition()
            active_petitions= active_petitions.query.filter(Petition.is_active == True).all()

            return jsonify(list(map(lambda item: item.serialize(), active_petitions))) , 200
        else:
            petition = Petition()
            petition = petition.query.get(petition_id)
            if petition:
                return jsonify(petition.serialize())
            
        return jsonify({"message":" Petition has not found"}), 404 
    
#ADD PETITIONS
@app.route('/petition', methods=['POST'])
@jwt_required()
def add_petition():
    if request.method == 'POST':
        body = request.json

        code = body.get('code', None)
       
        document_title = body.get('document_title', None)
        change_description = body.get('change_description', None)
        change_justify = body.get('change_justify', None)
        type_document = body.get('type_document', None)
        change_type = body.get('change_type', None)
        user_id = body.get('user_id', None)
        
        if body is None or code is None or document_title is None or change_description is None or change_justify is None or type_document is None or change_type is None:
            return jsonify ("Por favor verifica que complete todos los campos e intente de nuevo"),404
        else:
            request_petition = Petition(code=code, document_title=document_title, change_description=change_description, change_justify=change_justify, type_document=type_document, change_type=change_type, user_id=user_id)
            print ("este es el request :", request_petition)
            db.session.add(request_petition)
                           
            try:
                db.session.commit()
                return jsonify("good job bro (Y)!!"), 201
            except Exception as error:
                db.session.rollback(),500
    return jsonify(), 201


#UPDATE PETITIONS
@app.route('/petitions-active/<int:petition_id>', methods=['PATCH','PUT'])
@cross_origin()
@jwt_required()
def update_petition(petition_id=None):
    if request.method == 'PUT':
        body = request.json
        
        if petition_id is None:
            return jsonify({"message":"Bad request"}), 400

        if petition_id is not None:
            update_petition = Petition.query.get(petition_id)
            if update_petition is None:
                return jsonify({"message":"Not found"}), 404
            else:
                update_petition.code = body["code"] 
                update_petition.change_description = body["change_description"]
                update_petition.change_justify = body["change_justify"]
                update_petition.type_document = body["type_document"]
                update_petition.change_type = body ["change_type"]
                update_petition.is_active = body["is_active"]

                try:
                    db.session.commit()
                    return jsonify(update_petition.serialize()), 201
                except Exception as error:
                    print(error.args)
                    return jsonify({"message":f"Error {error.args}"}),500
        return jsonify([]), 200            
    elif request.method == 'PATCH':
        if petition_id is None:
            return jsonify({"message":"Bad request"}), 400

        if petition_id is not None:
            update_petition = Petition.query.get(petition_id)
            if update_petition is None:
                return jsonify({"message":"Not found"}), 404
            
            data = request.get_json()
            try:
                if'code' in data:
                    update_petition.code = data["code"]
                if 'document_title' in data:   
                    update_petition.document_title = data["document_title"]
                if 'change_description' in data:
                    update_petition.change_description = data["change_description"]
                if 'change_justify' in data:
                    update_petition.change_justify = data["change_justify"]
                if 'type_document' in data:
                    update_petition.type_document = data["type_document"]
                if 'change_type' in data:
                    update_petition.change_type = data ["change_type"]
                if 'is_active' in data:
                    update_petition.is_active = data["is_active"]
                db.session.commit()   
                return jsonify({'message': 'Petition replaced successfully'}), 202 
            except Exception as error:
                print(error.args)
                return jsonify({"message":f"Error {error.args}"}),500
        return jsonify([]), 200
    return jsonify([]), 405

#DELETE PETITION
@app.route('/petitions-active', methods=(['DELETE']))
@app.route('/petitions-active/<int:petition_id>', methods=['DELETE'])
@jwt_required()
@roles_required('admin','calidad') 
def delete_petition(petition_id):
    if request.method == 'DELETE':
        request.body = request.json

        if petition_id is None:
            return jsonify("the petition doesn`t exist :("), 400
        
        if petition_id is not None:
            delete_petition = Petition.query.get(petition_id) 
            print ("peticion:",delete_petition)

            if delete_petition is None:
                return jsonify({"Message":"Petition no found"})
            else:
                db.session.delete(delete_petition)

                try:
                    db.session.commit()
                    return jsonify("Petition has been deleted succesfully")
                except Exception as error:
                    print(error.args)
                    db.session.rollback()
                    return jsonify({"message":f"Error {error.args}"}),500
                
#CONSULT CONTROLP ACTIVE

@app.route('/controlsp', methods=['GET'])
@app.route('/controlsp/<int:controlp_id>', methods=['GET'])
@jwt_required()
def handle_controlp(controlp_id = None):
    if request.method == 'GET':
        
        if controlp_id is None:
            controls_p = PetitionControl()
            controls_p= controls_p.query.all()

            return jsonify(list(map(lambda item: item.serialize(), controls_p))) , 200
        else:
            control_p = PetitionControl()
            control_p = control_p.query.get(controlp_id)
            if control_p:
                return jsonify(control_p.serialize())
            
        return jsonify({"message":" Petition has not found"}), 404 
    



#ADD CONTROLP 

@app.route('/controlp', methods=['POST'])
@cross_origin()
@jwt_required()
def add_controlp():
    if request.method == 'POST':
        body = request.json
             
        process_affected = body.get('process_affected', None)
        name_customer = body.get('name_customer', None)
        process_customer = body.get('process_customer', None)
        status = body.get('status', None)
        date_petition_sent = body.get('date_petition_sent', None)
        date_petition_received = body.get('date_petition_received', None)
        date_finished_petition = body.get ('date_finished_petition', None)
        observation= body.get('observation', None)
        petition_id= body.get('petition_id', None)
        
        if body is None or process_affected is None or name_customer is None or process_customer is None or status is None or date_petition_sent is None or date_petition_received is None or observation is None:
            return jsonify ("Por favor verifica que complete todos los campos e intente de nuevo"),404
        else:
            request_petition_control = PetitionControl(process_affected=process_affected, name_customer=name_customer, process_customer=process_customer, status=status, date_petition_sent=date_petition_sent, date_petition_received=date_petition_received, date_finished_petition=date_finished_petition, observation=observation, petition_id= int(petition_id))
            print ("este es el request :", request_petition_control)
            db.session.add(request_petition_control)

                           
            try:
                db.session.commit()
                return jsonify("good job bro (Y)!!"), 201
            except Exception as error:
                db.session.rollback(),500

        
    return jsonify(), 201


#UPDATE CONTROLP 

@app.route('/controlsp/<int:controlp_id>', methods=['PATCH', 'PUT'])
@cross_origin()
@jwt_required()
def update_controlp(controlp_id=None):
    if request.method == 'PUT':
        body = request.json
        
        if controlp_id is None:
            return jsonify({"message":"Bad request"}), 400

        if controlp_id is not None:
            update_controlp = PetitionControl.query.get(controlp_id)
            if update_controlp is None:
                return jsonify({"message":"Not found"}), 404
            else:
                update_controlp.process_affected = body["process_affected"]
                update_controlp.name_customer = body["name_customer"]
                update_controlp.process_customer = body["process_customer"]
                update_controlp.date_petition_sent = body["date_petition_sent"]
                update_controlp.status = body["status"]
                update_controlp.date_petition_received = body ["date_petition_received"]
                update_controlp.date_finished_petition = body ["date_finished_petition"]
                update_controlp.observation = body ["observation"]
                update_controlp.petition_id = body ["petition_id"]
                

                try:
                    db.session.commit()
                    return jsonify(update_controlp.serialize()), 201
                except Exception as error:
                    print(error.args)
                    return jsonify({"message":f"Error {error.args}"}),500                 
    elif request.method == 'PATCH':
        if  controlp_id is None:
            return jsonify({"message":"Bad request"}), 400

        if controlp_id is not None:
            update_controlp = PetitionControl.query.get(controlp_id)
            if update_controlp is None:
                return jsonify({"message":"Not found"}), 404
            
            data = request.get_json()
            try:
                if 'process_affected' in data:
                    update_controlp.process_affected = data["process_affected"]
                if 'name_customer' in data:   
                    update_controlp.name_customer = data["name_customer"]
                if 'process_customer' in data:
                    update_controlp.process_customer = data["process_customer"]
                if 'date_petition_sent' in data:
                    update_controlp.date_petition_sent = data["date_petition_sent"]
                if 'status' in data:
                    update_controlp.status = data["status"]
                if 'date_petition_received' in data:
                    update_controlp.date_petition_received = data["date_petition_received"]
                if 'date_finished_petition' in data:
                    update_controlp.date_finished_petition = data ["date_finished_petition"]
                if 'observation' in data:
                    update_controlp.observation = data["observation"]
                if 'petition_id' in data:
                    update_controlp.petition_id = data["petition_id"]
                db.session.commit()   
                return jsonify({'message': 'ControlP replaced successfully'}), 202 
            except Exception as error:
                print(error.args)
                return jsonify({"message":f"Error {error.args}"}),500
        return jsonify([]), 200        
      
    return jsonify([]), 405



#DELETE CONTROLP

@app.route('/controlsp', methods=(['DELETE']))
@app.route('/controlsp/<int:controlp_id>', methods=['DELETE'])
@jwt_required()
def delete_controlp(controlp_id):
    if request.method == 'DELETE':
        request.body = request.json

        if controlp_id is None:
            return jsonify("the petition doesn`t exist :("), 400
        
        if controlp_id is not None:
            delete_controlp = PetitionControl.query.get(controlp_id) 
            print ("peticion:",delete_controlp)

            if delete_controlp is None:
                return jsonify({"Message":"Petition no found"})
            else:
                db.session.delete(delete_controlp)

                try:
                    db.session.commit()
                    return jsonify("Petition has been deleted succesfully")
                except Exception as error:
                    print(error.args)
                    db.session.rollback()
                    return jsonify({"message":f"Error {error.args}"}),500


















































############PRUEBA
                







                
@app.route('/game', methods=['POST'])
@jwt_required()
def add_game():
    if request.method == 'POST':
        body = request.json

        name_game = body.get('name_game', None)
        type_game = body.get('type_game', None)
        
        if name_game is None or type_game is None:
            return jsonify ("Por favor verifica que complete todos los campos e intente de nuevo"),404
        else:
            request_game = Game(name_game=name_game, type_game=type_game)
            print ("este es el request :", request_game)
            db.session.add(request_game)
                           
            try:
                db.session.commit()
                return jsonify("good job bro (Y)!!"), 201
            except Exception as error:
                db.session.rollback(),500
    return jsonify(), 201



@app.route('/game', methods=['GET'])
@app.route('/game/<int:game_id>', methods=['GET'])
@jwt_required()
def handle_game(game_id = None):
    if request.method == 'GET':
        
        if game_id is None:
            games = Game()
            games= games.query.all()

            return jsonify(list(map(lambda item: item.serialize(), games))) , 200
        else:
            game = Game()
            game = game.query.get(game_id)
            if game:
                return jsonify(game.serialize())
            
        return jsonify({"message":" Petition has not found"}), 404 




if __name__ == '__main__':
    APP_PORT= os.getenv('APP_PORT')
    app.run(port=APP_PORT, debug=True)

