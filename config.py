from decouple import config


class Config:
    SECRET_KEY = 'adsi' 

class DevelopmentConfig(Config): 
 
    motor = 'mysql://'
    user_db = 'sena:'
    password_db = 'sena123@'
    server = 'localhost/'
    name_db = 'project_web'

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = motor + user_db + password_db + server + name_db
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS =True
    MAIL_USERNAME = 'called691@gmail.com'
    MAIL_PASSWORD = ('3217576343a') 

config = { 
    'development': DevelopmentConfig, 
    'default' : DevelopmentConfig
    }
