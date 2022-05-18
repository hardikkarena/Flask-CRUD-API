from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow 

app = Flask(__name__)
ma = Marshmallow(app)

# Database Configrations
app.secret_key = "abc"  
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///databse/blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#Database Classes
db = SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    posts = db.relationship('Post', backref='user')
    def __repr__(self) -> str:
        return f"{self.first_name} - {self.last_name}"

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    date_created=db.Column(db.DateTime(500),default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"  

#Database Schema For Serialization
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'first_name', 'last_name', 'email', 'password')
user_schema = UserSchema(many=False)
users_schema = UserSchema(many=True)

class PostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'description', 'user_id', 'date_created')
post_schema = PostSchema(many=False)
posts_schema = PostSchema(many=True)