from flask import Flask, jsonify,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from models import app,db,User,Post,user_schema,users_schema,post_schema,posts_schema
# print("sdfs")
#Inedx Or Landing Page
@app.route("/",methods=['GET'])
def index():
    user = User.query.all()
    post = Post.query.all()
    data=[user,post]
    return render_template("index.html",data=data)

'''
    register api :
    - user will pass first_name,last_name,email,password in json fromat
    - in server site we'll check if email which is entered by user is 
       already exist or not.
    - if user is  already exist then it'll return error with status code 501
    - else we create new user in databse and return that data in json fromat with status code 201

'''
@app.route("/register",methods=['POST'])
def register():
    if request.content_type == 'application/json':
        
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']
        # isUsernameexist = User.query.filter_by(email=email)
        isUsernameexist=bool(User.query.filter_by(email=email).first())
        if isUsernameexist:
            return jsonify('User Already Exist'),501
        else:
            new_user = User(first_name=first_name,last_name=last_name,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return user_schema.jsonify(new_user),201

'''
    login api :
    - user will email & password in json fromat
    - in server site we'll check if email which is entered by user is 
       already exist or not.
    - if user exist then we'll match passwords from database & from user 
    - if passwords match we'll create session of user id & return user 
      in json format with status code 202
    - id password dose not matched then we'll return error with status code 401

'''
@app.route("/login",methods=['POST'])
def login():
    if request.content_type == 'application/json':
        email = request.json['email']
        password = request.json['password']
        
        # isUsernameexist = User.query.filter_by(email=email)
        
        isUsernameexist=bool(User.query.filter_by(email=email).first())
        if isUsernameexist:
            user = User.query.filter_by(email=email).first()
            if user.password == password:
                session['id']=user.id
                print(session['id'])
                return user_schema.jsonify(user),200
            else:
                return jsonify('Invalide Password'),401
        else:
            return jsonify('Invalide Email'),401

''''
    logout api :
    - when we call logout api
    - it'll delete session and return messege with status code 200
'''
@app.route("/logout")
def logout():
    session.pop('id',None) 
    return jsonify('User Logout'),200

'''
    /post/create api
    - user will title & description in json fromat
    - in server site we'll first we check user login or not
    - if user is not login we'll return error with status code 501
    - else we create user from sesion id and create new post in
      databse 
    - and return it in json format with status code 201
'''
@app.route("/post/create",methods=['POST'])
def post_create():
    
    if request.content_type == 'application/json':
        
        if 'id' in session:  
            user_id = bool(session['id'])
            user=User.query.get(user_id)
            print(user)
            title = request.json['title']
            dec = request.json['description']
            new_post = Post(title=title,description=dec,user_id=user.id)
            db.session.add(new_post)
            db.session.commit()
            return post_schema.jsonify(new_post),201
        else:
            return jsonify('User Not Login'),501

'''
    post api
    - it'll call with get method and in get method we'll pass id of post
    - usig that is from get methof it'll check post exist or not
    - if post not exist we'll error with status code 404
    - if post exist than fatch post from databse and return with status code 200
'''
@app.route("/post/<id>",methods=['GET'])
def post(id):
    try:
        posts = Post.query.get(id)
        result = post_schema.dump(posts)
        return jsonify(result),200
    except:
         return jsonify('ID Not Found'),404

'''
    posts api
    - it'll call with get method 
    - then fatch all posts from databse and return it with status code 200
'''
@app.route("/posts",methods=['GET'])
def posts():
    posts = Post.query.all()
    result = posts_schema.dump(posts)
    return jsonify(result),200
'''
    update_post api
    - it'll call with PUT method with  data id title & description
    - using id we'll fatch that post and update it and
      return it with status code 202

'''
@app.route('/post/update/<id>', methods=['PUT'])
def update_post(id):
    try:
        post = Post.query.get(id)
        post.title = request.json['title']  
        post.description = request.json['description']  
        db.session.commit()
        return post_schema.jsonify(post),202
    except:
         return jsonify('ID Not Found'),404

'''
    delete_post api
    - it'll call with DELETE method with  data id 
    - using id we'll fatch that post and delete it and
      return massge with status code 200

'''
@app.route('/post/delete/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify('Post Deleted'),200
    except:
         return jsonify('Pass Valide ID'),404


if __name__ == "__main__":
    app.debug=True
    app.run()