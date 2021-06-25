import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash 
from . import db 

class User(db.Model, UserMixin): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(102), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(50), unique = True, nullable = False)
    user_photo = db.Column(db.String(50), unique = True, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now()) 
    articles = db.relationship('Article', lazy='dynamic') 

    def verify_password(self, password): 
        return check_password_hash(self.encrypted_password,password) 
    @property
    def password(self): 
        pass 
    @password.setter 
    def password(self,value):
        self.encrypted_password = generate_password_hash(value) 

    def __str__(self):
        return self.username

    @classmethod 
    def create_element(cls,username,password,email,mobile,user_photo):
        user = User(username = username, password = password, email = email, mobile = mobile, user_photo = user_photo)
        db.session.add(user) 
        db.session.commit() 
        return user

    @classmethod 
    def get_by_username(cls, username): 
        return User.query.filter_by(username=username).first() 

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod 
    def get_by_id(cls, id):
       return User.query.filter_by(id=id).first()

class Article(db.Model): 
    __tablaname__ = 'articles' 

    id = db.Column(db.Integer, primary_key=True)
    article_photo = db.Column(db.String(50),nullable = True)
    name_article = db.Column(db.String(50))
    article_description = db.Column(db.Text())
    article_address = db.Column(db.String(50))
    article_expires = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    created_at = db.Column(db.DateTime, default=datetime.datetime.now()) 

    @property
    def little_description(self):
        if len(self.description)>20: 
            return self.description[0:19]+"..." 
        return self.descripcion
    @classmethod 
    def create_element(cls, article_photo, name_article, article_description, article_address, article_expires, user_id ):
        article=Article(article_photo=article_photo, name_article=name_article, article_description=article_description, article_address=article_address, article_expires=article_expires, user_id=user_id)

        db.session.add(article)
        db.session.commit()

        return article

    @classmethod 
    def get_by_id(cls, id):
        return Article.query.filter_by(id=id).first()

    @classmethod 
    def update_element(cls, id, article_photo, name_article,article_description, article_address,article_expires): 
        article = Article.get_by_id(id)
        if article is None: 
            return False

        article.article_photo = article_photo 
        article.name_article = name_article
        article.article_description  = article_description 
        article.article_address  = article_address 
        article.article_expires  = article_expires  

        db.session.add(article)
        db.session.commit()

        return article

    @classmethod 
    def delete_element(cls, id):
        article = Article.get_by_id(id)

        if article is None:
            return False

        db.session.delete(article) 
        db.session.commit()

        return True
