from datetime import datetime, timedelta
import hashlib, jwt, werkzeug
from flask.helpers import url_for
from flask import request, session, url_for, make_response
import logging

from flask.cli import DispatchingApp

from flask.json import jsonify
from flask import app, request, make_response,Response
from flask.templating import render_template
from werkzeug.utils import redirect
from models import *
from functools import wraps

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# If you programmatically wants to create the database then use create_all() function
db.create_all()
db.session.commit()

app.config['SECRET_KEY'] = 'keyissecured12123'
token=''

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = request.args.get('jwt') 
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            print(data)
            current_user = data['user']

        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

#First Flask code to display Hello World
@app.route('/test')
def hello_world():
    return "Hello World"


#Create an index page
@app.route('/')
def indexPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('index.html')


#creating login page
@app.route('/login/')
def loginPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('login.html')

#creating admin page
@app.route('/admin/')
def adminPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('adminlogin.html')

#creating admin page
@app.route('/adminpage')
def adminFormPage():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return render_template('adminForm.html')


#creating register page
@app.route('/register/')
def registerPage():
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    return render_template('register.html')

@app.route('/registersuccess', methods=["POST"])
def registerSuccess():
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        #hashing the password before storing
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()

        entry = Users(name=name,email=email,password=hashedPassword, username=username)
        db.session.add(entry)
        db.session.commit()
    return render_template('login.html')


@app.route('/editsuccess', methods=["POST"])
def editSuccess():
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    if request.method == "POST":
        id = request.form.get('id')
        title = request.form.get('title')
        categories = request.form.get('categories')
        tags = request.form.get('tags')
        link = request.form.get('link')
        type = request.form.get('type')
        featured = request.form.get('featured')
        level = request.form.get('level')

        entry = AdminSuccess(id=id,title=title,categories=categories, tags=tags, link=link, type=type,featured=featured, level=level)
        db.session.add(entry)
        db.session.commit()
    return render_template('dashboard.html')

@app.route('/loginsuccess', methods=['POST'])
def loginSucess():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #hashing the input and comparing the hash
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        result = db.session.query(Users).filter(Users.email==email, Users.password==hashedPassword)
        for row in result:
            if (len(row.email)!=0):
                print(row.email)
                token = jwt.encode({'user':row.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
                token= token.decode('utf-8')
                # return redirect(url_for('dashboard'))
                # session['jwt']=token
                return make_response(jsonify({'jwt':token}), 201)
    return make_response('could not verify', 401, {'WWW-Authenticate':'Basic="Login Required"'})

@app.route('/adminsuccess', methods=['POST'])
def adminSucess():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(password)
        #hashing the input and comparing the hash
        hashedPassword = hashlib.md5(password.encode())
        # result = hashlib.md5(str2hash.encode())
        hashedPassword = hashedPassword.hexdigest()
        result = db.session.query(Admins).filter(Admins.email==email, Admins.password==password)
        for row in result:
            if (len(row.email)!=0):
                print(row.email)
                # token = jwt.encode({'user':row.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
                # print("Token ",token)
                # token= token.decode('utf-8')
                # session['jwt']=token
                # return redirect(url_for('adminpage'))
                return render_template("adminForm.html")
                # return make_response(jsonify({'jwt' : token}), 201)
    return render_template("index.html")
    # return make_response('could not verify', 401, {'WWW-Authenticate':'Basic="Login Required"'})


@app.route('/dashboard')
@token_required
def dashboard(current_user): # http://127.0.0.1:8000/dashboard?jwt=
    return render_template('dashboard.html', data=current_user)

@app.errorhandler(werkzeug.exceptions.BadRequest)
def badRequest(e):
    # app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    return "Bad request", 400
app.register_error_handler(400, badRequest)

@app.errorhandler(404)
def notFound(e):
    return "Page not found", 404
app.register_error_handler(404,notFound )

#Check for the docs of error https://flask.palletsprojects.com/en/2.0.x/errorhandling/
#HTTP Codes https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

if __name__ == "__main__":
    app.run(debug=True, port=8001)

#logging -> reference https://www.askpython.com/python-modules/flask/flask-logging
# Five levels of debugging
# debug, info, warning, error, critical
