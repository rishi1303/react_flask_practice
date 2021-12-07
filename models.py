from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost/flasksample"
db = SQLAlchemy(app)


class Users(db.Model):
    # you can even specify the table name with which you are working.
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), unique = False, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    
class Admins(db.Model):
    # you can even specify the table name with which you are working.
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), unique = False, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
class AdminSuccess(db.Model):
    # you can even specify the table name with which you are working.
    __tablename__ = 'adminSuccess'
    id = db.Column(db.Integer, primary_key = True, unique=True, nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    categories = db.Column(db.String(200), unique=True, nullable=False)
    tags = db.Column(db.String(100), unique=True, nullable=False)
    link = db.Column(db.String(500), unique = False, nullable=False)
    type = db.Column(db.String(200), unique=True, nullable=False)
    featured = db.Column(db.String(200), unique=True, nullable=False)
    level = db.Column(db.String(200), unique=True, nullable=False)
    