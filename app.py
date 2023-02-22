from flask import Flask, request, render_template, redirect, url_for, make_response, flash
from flask_sock import Sock
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import secrets
import string
import hashlib
import json
from os import environ
import mysql.connector



sqldb = mysql.connector.connect(
    host= "mysql",
    user= "yrden1" ,
    database= "db",
    password =  "password1"

)


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://yrden1:password1@mysql/db'
app.config['SECRET_KEY'] = "super secret key"
#mysql://username:password@server/db

db= SQLAlchemy(app)

#db_cursor = sqldb.cursor()
#db_cursor.execute("CREATE TABLE IF NOT EXISTS users ( name TEXT,hashedpassword TEXT, salt TEXT")
#db_cursor.execute("CREATE TABLE IF NOT EXISTS authentication ( username TEXT,hashedtoken TEXT")
#db_cursor.execute("CREATE TABLE IF NOT EXISTS messages (name TEXT, name TEXT,_id hashedpassword, name salt")

sock = Sock(app)

connections = []
userconn={}
chat_history=[]

print("almost")

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name= db.Column("name", db.String(100))
    hashedpassword = db.Column("hashedpassword", db.String(100))
    salt = db.Column("salt", db.String(100))


    def __init__(self, name, hashedpassword, salt):
        self.name = name
        self.hashedpassword = hashedpassword
        self.salt = salt

#auth_token_collection.insert_one({"username": user.decode(), "token": hashedtoken})
class authentication(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username= db.Column("username", db.String(100))
    token = db.Column("token", db.String(100))

    def __init__(self, name, tkn):
        self.username = name
        self.token = tkn

class messages(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name= db.Column("name", db.String(100))
    comment = db.Column("comment", db.String(100))

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment


@app.route('/')
def index():
    token = request.cookies.get('idcookie')
    hashedcookie = hashlib.sha256(str(token).encode()).hexdigest()
    trustr=isvalid(hashedcookie)
    if trustr==True:
        name2 = authentication.query.filter_by(token=hashedcookie).first()
        username= str(name2.username)
        response = make_response(render_template('chat.html'))
        return response
      

    response =  make_response(render_template('index.html'))
    return response

@app.route('/login')
def login():
    response =  make_response(render_template('login.html'))
    response.set_cookie('userexists', 'False')
    return response

@app.route('/register', methods=["POST"])
def register():
    password1=request.form["password"].encode('utf-8')
    salt1 = bcrypt.gensalt()
    hashedpassw = bcrypt.hashpw(password1, salt1)
    user = users(
        name=request.form["uname"],
        hashedpassword= hashedpassw.decode(),
        salt=  salt1.decode()
    )
    name1 = request.form["uname"]
    exists = db.session.query(db.exists().where(users.name == name1)).scalar()
    if exists==False:
        db.session.add(user)
        db.session.commit()
        response = make_response(redirect(url_for('login')))
        response.set_cookie('userexists', 'False')
        return response
    else:

        response = make_response(redirect(url_for('index')))
        response.set_cookie('userexists', 'True')
        return response

@app.route('/loginstart', methods=["POST"])
def loginstart():
    name1 = request.form["uname2"]
    password1=request.form["password"]
    exists = db.session.query(db.exists().where(users.name == name1)).scalar()
    print(exists)
    if exists==True:
        print("crash")
        name2 = users.query.filter_by(name=name1).first()
        salt= str(name2.salt)
        saltedhash = str(name2.hashedpassword)
        hashedpassw = bcrypt.hashpw(password1.encode(), salt.encode())
        print(saltedhash)
        print(hashedpassw)
        if saltedhash==hashedpassw.decode():
            flash('Succesful login')
            
            alphabet = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
            token1= "".join(secrets.choice(alphabet) for i in range(18))
            hashedtoken = hashlib.sha256(token1.encode()).hexdigest()
            user = authentication(
                name=name1,
                tkn= hashedtoken,
            )
            db.session.add(user)
            db.session.commit()
            response = make_response(render_template('chat.html'))
            response.set_cookie('userexists', 'False')
            response.set_cookie('idcookie', value=token1, httponly = True, max_age=3600)
            response.set_cookie('name', value=name1,  max_age=3600)
            return response
        else:
            flash('wrong username or password')
            response = make_response(redirect(url_for('login')))
            response.set_cookie('userexists', 'False')
            return response
    else:
        response = make_response(redirect(url_for('login')))
        response.set_cookie('userexists', 'False')
        return response
@sock.route('/websocket')
def sendmessage(ws):
    token = request.cookies.get('idcookie')
    hashedcookie = hashlib.sha256(str(token).encode()).hexdigest()
    trustr=isvalid(hashedcookie)
    name2 = authentication.query.filter_by(token=hashedcookie).first()
    username= str(name2.username)
    
    
    for key, value in userconn.items():
        if(key==username):
            userconn[username]= ws

    if(userconn.get(username)==None):
        userconn[username]= ws

    while True:
        token = request.cookies.get('idcookie')
        hashedcookie = hashlib.sha256(str(token).encode()).hexdigest()
        trustr=isvalid(hashedcookie)
        if trustr==True:
            x=messages.query.all()
            for i in x:
                sendmsg= {}
                sendmsg["messageType"]= 'chatMessage'
                sendmsg["username"]=i.name
                sendmsg["comment"]= i.comment
                sendmsg = json.dumps(sendmsg)

                for key, value in userconn.items():
                    value.send(sendmsg)

            print(x)
            

            name2 = authentication.query.filter_by(token=hashedcookie).first()
            username= str(name2.username)
            
            text= ws.receive()
            if(len(text)!=0):

                message = json.loads(text)
                msgtype = message["messageType"]
                msg= message["comment"]
                msg = msg.replace('&',"&amp;").replace('<',"&lt;").replace('>',"&gt;")

                message = messages(
                    name=username,
                    comment=msg,
            
                )
                db.session.add(message)
                db.session.commit()
                sendmsg= {}
                sendmsg["messageType"]= msgtype
                sendmsg["username"]=username
                sendmsg["comment"]= msg
                sendmsg = json.dumps(sendmsg)

                for key, value in userconn.items():
                    value.send(sendmsg)
            

  
    





        
def isvalid(tkn):
    print(tkn)
    exists = db.session.query(db.exists().where(authentication.token == tkn)).scalar()
    if(exists==True):
        return True
    else:
        return False
        





if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=8080)
