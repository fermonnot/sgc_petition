
from flask  import Flask
from enum import Enum
from sqlalchemy import Enum as EnumType
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from alembic import op
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash




db = SQLAlchemy()



class User (db.Model):

    __tablename__='user_table'

    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), unique=True, nullable=False)
    roles_user= db.Column(EnumType('usuario', 'calidad', 'admin', name='role'))
    petition= db.relationship('Petition', back_populates='user')


    def __repr__(self):
        return f'<User {self.user_name, self.roles_user}>'

    def serialize(self):
        return{
            "id": self.id,
            "name": self.user_name,
            'roles_user': self.roles_user
        }


class Petition(db.Model):

    __tablename__='petitions'
     
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    code = db.Column(db.String (150), nullable = False)
    document_title = db.Column(db.String(150), nullable = False)
    change_description = db.Column(db.String(150), nullable = False)
    change_justify = db.Column(db.String(150), nullable = False)
    type_document = db.Column(EnumType('formulario','procedimiento','instrucciont','otro', name= 'type_document'))
    change_type = db.Column (EnumType('creacion','actualizacion','eliminacion', name = 'change_type'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    user = db.relationship("User", back_populates='petition')
    petitioncontrol = db.relationship('PetitionControl', back_populates='petition')
    

    def __repr__(self):
        return f'<Petition {self.code, self.document_title, self.change_description, self.change_justify, self.type_document,self.change_type, self.user_id}>'

    def serialize(self):
        return{
            "id": self.id,
            "code": self.code,
            'document_title': self.document_title,
            "change_description": self.change_description,
            "change_justify": self.change_justify,
            "type_document":self.type_document,
            "change_type": self.change_type,
            "user_id": self.user_id
        }


class PetitionControl(db.Model):

    __tablename__='petition_control'

    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    date_petition = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    process_affected =db.Column (db.String(100), nullable = False)
    name_customer = db.Column (db.String(100), nullable = False)
    process_customer = db.Column (db.String(100), nullable = False)
    date_petition_sent = db.Column (db.String(100), nullable = False)
    status = db.Column ((EnumType('divulgado','distribuido','completado', name = 'status')))
    date_petition_received = db.Column (db.String(100), nullable = False)
    date_finished_petition = db.Column (db.String (100), nullable= False)
    observation = db.Column (db.String (100))
    petition_id= db.Column (db.Integer, db.ForeignKey('petitions.id'))
    petition = db.relationship('Petition', back_populates='petitioncontrol')
    
    # petition= db.relationship('Petition', back_populates= 'petitioncontrol')

    def __init__(self, process_affected, name_customer, process_customer, status, date_petition_sent, date_petition_received, date_finished_petition, observation, petition_id):
        self.date_petition: datetime.utcnow()
        self.process_affected: process_affected
        self.name_customer: name_customer
        self.process_customer: process_customer
        self.status: status
        self.date_petition_sent: date_petition_sent 
        self.date_petition_received : date_petition_received
        self.date_finished_petition: date_finished_petition 
        self.observation: observation 
        self.petition_id: petition_id

    def __repr__(self):
        return f'<PetitionControl {self.date_petition, self.process_affected, self.name_customer,self.process_customer, self.status, self.date_petition_sent,self.date_petition_received,self.date_finished_petition, self.observation, self.petition_id}>'

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
            "petition_id": self.petition_id
        }

    