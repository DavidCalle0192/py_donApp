from flask import Blueprint 
from flask import render_template, request, flash, redirect, url_for,abort
from .forms import LoginForm, RegisterForm, TaskForm
from .models import User, Article 
from flask_login import login_user, logout_user, login_required, current_user
from .consts import *
from .email import welcome_mail
from . import login_manager

import os
from werkzeug.utils import secure_filename
from flask import Flask,send_from_directory
#UPLOAD_FOLDER = os.path.abspath("./images/")



page = Blueprint('page', __name__) 

#page.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@login_manager.user_loader
def load_user(id): 
    return User.get_by_id(id)

@page.app_errorhandler(404) 
def page_not_found(error): 
    return render_template('errors/404.html'), 404  


@page.route('/')
def index():
    return render_template('index.html', title='Index')

@page.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT)
    return redirect(url_for('.login')) 

@page.route('/login', methods=['GET','POST']) 
def login():

    if current_user.is_authenticated: 
        return redirect (url_for('.articles'))

    form = LoginForm(request.form) 

    if request.method == 'POST' and form.validate(): 
        user=User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data): 
            login_user(user)
            flash(LOGIN)
        else:
            flash(ERROR_USER_PASSWORD,'error' )
    return render_template('auth/login.html', title= 'Login', form = form, active='login')

@page.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated: 
        return redirect (url_for('.articles'))

    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate():
            user = User.create_element(form.username.data, form.password.data, form.email.data, form.mobile.data, form.user_photo.data)
            flash(USER_CREATED)
            login_user(user)
            welcome_mail(user)
            return redirect(url_for('.articles'))

    return render_template('auth/register.html', title ='Registro', form = form, active='register')

@page.route('/articles')
@page.route('/articles/<int:page>')
@login_required
def articles(page=1, per_page=2): 
    pagination = current_user.articles.paginate(page, per_page=per_page)
    articles = pagination.items

    return render_template('articles/food_items/list.html', title='Tareas', articles=articles, pagination=pagination, page=page, active='articles')

@page.route('/articles/new', methods=['GET','POST']) 
@login_required 
def new_article():
    form = TaskForm(request.form)

    if request.method == 'POST' and form.validate():
        article = Article.create_element(form.article_photo.data,form.name_article.data, form.article_description.data,form.article_address.data,form.article_expires.data, current_user.id)

        if article:
            flash(TASK_CREATED)
    return render_template('articles/food_items/new.html', title='Nueva tarea', form=form, active='new_article')

@page.route('/articles/food_items/show/<int:article_id>')  
def get_article(article_id):
    article=Article.query.get_or_404(article_id)
    return render_template('articles/food_items/show.html', title='Tarea', article=article)


@page.route('/articles/food_items/edit/<int:article_id>', methods=['GET','POST'])
@login_required
def edit_article(article_id):

    article=Article.query.get_or_404(article_id) 

    if article.user_id != current_user.id: 
        abort(404)
    form=TaskForm(request.form, obj=article) 
    if request.method=='POST' and form.validate():
        article = Article.update_element(article.id,form.article_photo.data,form.name_article.data,form.article_description.data,form.article_address.data,form.article_expires.data)
        if article:
            flash(TASK_UPDATE)
    return render_template('articles/food_items/edit.html', title='Edit Article', form=form)

@page.route('/articles/food_items/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)

    if article.user_id != current_user.id: 
        abort(404)

    if Article.delete_element(article.id):
        flash(TASK_DELETE)
    return redirect(url_for('.articles'))



#""""""""""""""""""""""""""""""""""""""""""""""""""""""    
'''
@page.route("/upload", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        try:
            file.save(os.getcwd() + "/images/" + file.filename)
            return "Imagen guardada"
        except FileNotFoundError:
            return "Folder no existe"

@page.route('/image/<string:filename>')
def get_image(filename):
    return send_from_directory(os.getwd() + "/images/", filename = filename, as_attachment = False)




@page.route("/upload", methods =["GET", "POST"])
def upload():
    if request.method == 'POST':
        f = request.files["ourfile"]
        filename = f.filename
        f.save()'''