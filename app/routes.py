import imp
from flask_login import LoginManager, current_user, login_required, login_user, logout_user #импорты для flask-login

from app import app, db, icons_location #импортируем приложение фласк для работы с ним и базу данных

from flask import flash, redirect, render_template, request, url_for

from forms import * #импортирую формы для входа на страницу 

from models import * 

from flask_pagination import *

import os # нужно для работы с аватаркой


@app.route('/') #создаем путь на главную страницу
def index():
    if User.query.all() != []:
        last_user = User.query.all()[-1]
    else:
        last_user = []
    if Post.query.all() != []:
        last_post = Post.query.all()[-1]
    else: 
        last_post = []
    return render_template('index.html', last_user=last_user, last_post=last_post) #рендер делает обработку html файла


@app.route('/about/')
def about_page():
    return render_template('about.html')


@app.route('/tags/<link>/')
def tag_current(link):
    tag = Tag.query.filter_by(link=link).first()
    posts = tag.posts.all()
    return render_template('tag_detail.html', tag = tag, posts = posts)
    


@app.route('/login/', methods=['GET', 'POST']) #вызываю запрос для подачи данных и для взятия данных
def login():
    if current_user.is_authenticated: #если пользователь зарегистрирован
        return redirect(url_for('index')) #возращаю пользователя на функцию index
    
    form = LoginForm() #добавление всех form на страницу
    
    if form.validate_on_submit(): #проверяем все валидаторы 
        user = User.query.filter_by(username=form.username.data).first() #ищу пользователя в базе данных
        login_user(user, remember=form.remember_me.data) #логиню его через функцию login_user и запомнить меня
        return redirect(url_for('index')) #возвращаю на страницу профиля
    
    if form.errors != {}: #если в форме ValidationError не пустой словарь, то есть какая-та ошибка 
        for error in form.errors.values(): #делаем цикл из ошибок
            flash(''.join(error), category='error') #выводим ошибку с категорией danger
        
    return render_template('login.html', form=form) #страница login и передаем все формы
      
      
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #если пользователь зарегистрирован
        return redirect(url_for('index')) #возращаю пользователя на функцию index
    
    form = RegisterForm() #загрузка всех форм 
    
    if form.validate_on_submit(): #проверка все валидаторов 
        user = User(username=form.username.data, email=form.email.data, password=form.password.data) #создания нового пользователя 
        db.session.add(user) #добавление пользователя в сессию 
        db.session.commit() #сохранение сессии
        return redirect(url_for('login')) #возрашение на функицю логин
    
    if form.errors != {}: #если словарь ошибок не пустой 
        for error in form.errors.values(): #цикл для обработки каждой ошибки 
            flash(''.join(error), category='error') #вывод этих ошибок без скобок 
    
    return render_template('register.html', form=form)


@app.route('/logout/') #переход на страницу для выхода 
@login_required #страница только для авторизированых пользователей 
def logout():
    logout_user() #выход пользователя
    return redirect(url_for('login'))           

@app.route('/profile/')
@login_required
def profile_():
    return render_template('index')

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first() #находим пользователя из базы данных с таким-же ником
    post = Post.query.filter_by(user_id=user.id) #находим посты у которых id пользователя равно id страницы пользователя
    return render_template('profile.html', user=user, post=post)

@app.route('/profile/<username>/setting', methods=['GET', 'POST']) #настройки для профиля
@login_required
def profile_setting(username):
    form = Profileform() #формы для профиля
    user = User.query.filter_by(username=username).first() #находим пользователя с таким же ником
    
    if current_user.id != user.id: #если id текущего пользователя не совпадает с id пользователем из url адреса, то вывод ошибки
        flash('Вы не можете менять профиль другого человека!', category='error')
        return redirect(url_for('index'))
    
    if form.validate_on_submit(): #проверка валидаторов из формы 
        user.username, user.email, user.age, user.location, user.first_name, user.last_name, photo = \
        form.username.data, form.email.data, form.age.data, form.location.data, form.first_name.data, form.last_name.data, request.files['photo']
        db.session.commit() #меняем значения в базе данных и сохраняем их, request.files обязательно.
        
        if photo.filename != '': #если  пользователь добавил фотку, то
            photo.filename = f'{user.id}_icon.jpg' #создаем название файла как id пользователя_icon
            try:
                os.remove(os.path.join(icons_location, photo.filename)) #пытаемся найти дубликаты такого-же названия, если есть, то удаляем
            except:
                pass
            photo.save(os.path.join(icons_location ,photo.filename)) #сохраняем фотку в папке с названием, которое мы сделали
                                                                                                                                                                            
            user.icon = photo.filename #меняем в базе данных иконку пользователю
            db.session.commit() #сохраняем базу данных
        
        return redirect(url_for('profile', username = user.username))
    
    if form.errors != {}: #если валидатор формы вывел ошибку и список не пустой то
        for error in form.errors.values(): #цикл из ошибок
            flash(''.join(error), category='error') #выводим эти ошибки
    
    return render_template('profile_setting.html', user=user, form=form)

@app.route('/allprofile/') #все профили пользователей 
def allprofile():
    user = User.query.all() #вывод всех пользователей списком 
    return render_template('all_profile.html', user=user)

@app.route('/post/create/', methods=['GET', 'POST'])
@login_required #можно войти на страницу только зарегистрированным пользователям
def post_create():
    form = CreateForm()
    
    if form.validate_on_submit():
        title, body = form.title.data, form.body.data
    
        post = Post(title=title, body=body) #сохранение информации о посте в базу данных 
        db.session.add(post) # добавление в сессию, а потом сохранение
        db.session.commit()
        flash('Пост успешно создан!', category='success')
        return redirect(url_for('index'))
    
    if form.errors != {}: #перебор ошибок 
        for error in form.errors.values(): #цикл из ошибок
            flash(''.join(error), category='error') #их вывод
    
    return render_template('create_post.html', form=form)

@app.route('/posts')
def posts():
    search = request.args.get('search')
    page = request.args.get('page')
    
    if page and page.isdigit(): #если есть page и если она int
        page = int(page)
    else:
        page = 1
    
    if search:
        post = Post.query.filter(Post.title.contains(search) | Post.body.contains(search))
    else:
        post = Post.query.order_by(Post.time_created.desc())
    
    pages = post.paginate(page=page, per_page=4 ) #мы создаем пагинацию, где page=номер страницы, per_pages = количесвто постов на одну страницу. Я указал 5 штук 

    return render_template('posts.html', post=post, pages = pages)

@app.route('/post/detail/<link>')
def post_detail(link):
    post = Post.query.filter_by(link=link).first()
    tags = post.tags
    return render_template('post_detail.html', post=post, tags=tags)

@app.route('/post/<link>/settings', methods=['GET', 'POST'])
@login_required
def post_settings(link):
    form = EditPostForm()
    post = Post.query.filter_by(link=link).first()
    
    if current_user.id != post.user_id:
        flash('Вы не можете изменять пост, который создали не вы!', category='error')
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        post.title, post.body = form.title.data, form.body.data
        post.set_link()
        db.session.commit()
        
        flash('Вы успешно изменили пост!', category='success')
        return redirect(url_for('post_detail', link=post.link))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(''.join(error), category='error')
            
    
    return render_template('post_settings.html', post=post, form=form)

    
    
    
    
    