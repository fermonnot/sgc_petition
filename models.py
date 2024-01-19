
from flask  import Flask
from enum import Enum
import pytz
from sqlalchemy import Enum as EnumType
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from alembic import op
from datetime import datetime, timezone
from pytz import timezone
from sqlalchemy import event





db = SQLAlchemy()


def get_current_time():
   return datetime.now(pytz.timezone('America/Caracas'))


class User (db.Model):

    __tablename__='user_table'

    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=True, nullable=False)
    roles_user= db.Column(EnumType('usuario', 'calidad', 'admin', name='role'))
    petition= db.relationship('Petition', back_populates='user')


    def __repr__(self):
        return f'<User {self.id, self.user_name, self.roles_user}>'

    def serialize(self):
        return{
            "id": self.id,  
            "name": self.user_name,
            'roles_user': self.roles_user
        }


class Petition(db.Model):

    __tablename__='petitions'
     
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=get_current_time, nullable=False)
    code = db.Column(db.String (150), nullable = False)
    document_title = db.Column(db.String(150), nullable = False)
    change_description = db.Column(db.String(150), nullable = False)
    change_justify = db.Column(db.String(150), nullable = False)
    type_document = db.Column(EnumType('formulario','procedimiento','instrucciont','otro', name= 'type_document'))
    change_type = db.Column (EnumType('creacion','actualizacion','eliminacion', name = 'change_type'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    user = db.relationship("User", back_populates='petition')
    petitioncontrol = db.relationship('PetitionControl', back_populates='petition')
    is_active = db.Column(db.Boolean, default=True)
    

    def __repr__(self):
        return f'<Petition {self.created, self.code, self.document_title, self.change_description, self.change_justify, self.type_document,self.change_type, self.user_id, self.is_active}>'

    def serialize(self):
        return{
            "id": self.id,
            "created":self.created,
            "code": self.code,
            'document_title': self.document_title,
            "change_description": self.change_description,
            "change_justify": self.change_justify,
            "type_document":self.type_document,
            "change_type": self.change_type,
            "user_id": self.user_id,
            "is_active": self.is_active
        }


class PetitionControl(db.Model):

    __tablename__='petition_control'

    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    date_petition = db.Column(db.DateTime(timezone=True), default=get_current_time, nullable=False)
    process_affected =db.Column (db.String(100), nullable = False)
    name_customer = db.Column (db.String(100), nullable = False)
    process_customer = db.Column (db.String(100), nullable = False)
    date_petition_sent = db.Column (db.String(100), nullable = False)
    status = db.Column ((EnumType('divulgado','distribuido','completado', name = 'status')))
    date_petition_received = db.Column (db.String(100), nullable = False)
    date_finished_petition = db.Column (db.String (100), nullable= False)
    observation = db.Column (db.String (100))
    updated_at = db.Column(db.DateTime(timezone=True), default=get_current_time, onupdate=get_current_time, nullable=False)
    petition_id= db.Column (db.Integer, db.ForeignKey('petitions.id'))
    petition = db.relationship('Petition', back_populates='petitioncontrol')

    def set_timestamp(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    def __repr__(self):
        return f'<PetitionControl {self.date_petition, self.process_affected, self.name_customer,self.process_customer, self.status, self.date_petition_sent,self.date_petition_received,self.date_finished_petition, self.observation, self.updated_at, self.petition_id}>'

    def serialize(self):
        return{
            "id": self.id,
            "date_petition": self.date_petition,
            'process_affected': self.process_affected,
            "name_customer": self.name_customer,
            "process_customer": self.process_customer,
            "status":self.status, 
            "date_petition_sent": self.date_petition_sent,
            "date_petition_received": self.date_petition_received,
            "date_finished_petition": self.date_finished_petition,
            "observation": self.observation,
            "updated_at": self.updated_at,
            "petition_id": self.petition_id,
        }
    
    
    




class Game (db.Model):

    __tablename__='game'

    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    name_game = db.Column(db.String(120), unique=True, nullable=False)
    type_game = db.Column(db.String(300), unique=True, nullable=False)
    creado =  db.Column(db.DateTime(timezone=True), default=get_current_time, nullable=False)
    actualizado = db.Column(db.String(300), unique=True, nullable=False)
    
    


    def __repr__(self):
        return f'<User {self.id, self.name_game, self.type_game, self.creado, self.actualizado}>'

    def serialize(self):
        return{
            "id": self.id,  
            "name": self.name_game,
            'roles_user': self.type_game,
            'creado': self.creado,
            'actualizado': self.actualizado
        }
