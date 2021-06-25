from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms import validators

from .models import User

def user_validator(form, field): 
    if field.data=='adsi' or field.data=='Adsi':
        raise validators.ValidationError('El username adsi no es permitido')

class LoginForm(Form): 
    username = StringField('Username',[
        validators.length(min=4, max=50, message='El nombre de usuario debe encontrarse entre 4 y 50 caracteres de largo..')
    ])
    password = PasswordField('Password',[
        validators.Required(message='El password es requerido')
    ])

class RegisterForm(Form):
    username = StringField('Username',[
        validators.length(min=4, max=50),
        user_validator
    ])
    email = EmailField('Correo electronico',[
        validators.length(min=6, max=100),
        validators.Required(message='El email es requerido'),
        validators.Email(message='Ingrese un email valido')
    ])
    mobile = StringField('Mobile', [
        validators.length(min = 5, max = 100)
    ])
    user_photo = StringField('Photo', [
        validators.length(min = 5, max = 225)
    ])
    password = PasswordField('Password',[
        validators.Required('La contraseña es requerida.'),
        validators.EqualTo('confirm_password', message='La contraseña no coinside')
    ])
    confirm_password = PasswordField('Confirmar Contraseña')
    accept = BooleanField('Acepto terminos y condiciones',[
        validators.DataRequired()
    ])

    def validate_username(self, username): 
        if User.get_by_username(username.data): 
            raise validators.ValidationError('El usuario ya se encuentra registrado.') 

    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError('El email ya se encuentra registrado.')

    #def validate(self): #views line:38.
    #    if not Form.validate(self): 
    #        return False 

    #    if len(self.password.data) < 3 : 
    #        self.password.errors.append('La contraseña es muy corta') 
    #        return False 
    #    return True

class TaskForm(Form): 

    article_photo = StringField('Article Photo',[
        validators.DataRequired(message='The photo of the item is required')
    ])

    name_article = StringField('Naeme article',[
        validators.length(min=4, max=50, message = 'Name out of range'),
        validators.DataRequired(message='Name is required')
    ])

    article_description = TextAreaField('Description',[
        validators.DataRequired(message='Description is required.')
    ], render_kw = {'rows':5})

    article_address = StringField('Article Adress',[
        validators.DataRequired(message='The address where the item is located is required')
    ])

    article_expires = StringField('Article Expires',[
        validators.DataRequired(message='The expiration date of the item is required')
    ])

