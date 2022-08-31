from datetime import datetime

from sqlalchemy import ForeignKey #для рендеринга времени

from app import db, login_manager #из приложения импортируем базу данных, импортируем loginmanager

from werkzeug.security import check_password_hash, generate_password_hash #хэширование паролей

from flask_login import UserMixin, current_user #импортируем класс из Flask-login для работы над Пользователями 


@login_manager.user_loader # Он используется для проверки того, какой идентификатор пользователя находится в текущем сеансе, и загрузит пользовательский объект для этого идентификатора
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin): #Создание таблицы базы данных. Пользователи
    id = db.Column(db.Integer(), primary_key=True) #первичный ключ
    username = db.Column(db.String(20), unique=True, nullable=False) #уникальное значение, не может быть пустым
    email = db.Column(db.String(100), unique=True, nullable=False) #уникальное значение, не может быть пустым
    password = db.Column(db.Text()) #текст
    created = db.Column(db.DateTime(), default=datetime.utcnow) #дата когда создался пользователь 
    admin_role = db.Column(db.Integer(), default=0) #роль user
    
    icon = db.Column(db.String(200), default='default_icon.png') #иконка для профиля
    
    #необязательные персональные данные
    
    age = db.Column(db.Integer(), default='Не заполнено.')
    
    location = db.Column(db.Integer(), default='Не заполнено.')
    
    first_name = db.Column(db.String(50), default='Не заполнено.')
    
    last_name = db.Column(db.String(50), default='Не заполнено.')
    
    
    
    
    
    def __init__(self, *args, **kwargs): #при создании экземпляра класса будет выполнятся эта функция
        super(User, self).__init__(*args, **kwargs)
        self.create_password()
        
    def create_password(self): #хэшируется пароль
        self.password = generate_password_hash(self.password) #создание переменной где хранится хэшированый пароль
        
    def check_password(self, password):
        return check_password_hash(self.password, password) #возращает проверку пароля на верность 
    
    def __repr__(self): #как будет выглядить class в консоли
        return "<{}, {}, {}>".format(self.id, self.username, self.email)  

post_tags = db.Table('post_tags',
                    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
                    ) 
  
    
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True) #id поста 
    title = db.Column(db.String(140), nullable=False) #название поста
    body = db.Column(db.Text(), nullable=False) #описание поста
    
    time_created = db.Column(db.DateTime(), default=datetime.now()) #время когда создался пост
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id')) #
    user_username = db.Column(db.String(), db.ForeignKey('user.username'))
    link = db.Column(db.Text()) #ссылка для постов 

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    
    def __init__(self, *args, **kwargs): #при создании экземпляра класса будет выполнятся эта функция
        super(Post, self).__init__(*args, **kwargs)
        self.set_link() #
        self.add_tag()
        self.user_id = current_user.id #
        self.user_username = current_user.username
        

    def set_link(self):
        id = len(Post.query.filter_by(title=self.title).all()) + 1 #
        self.link = str(self.title.replace(' ', '_')) + '_' + str(id) #
        
    
    def add_tag(self):
        self.tags = []
        for tag in Tag.query.all():
            if tag.name in self.body or tag.name.lower() in self.body.lower():
                self.tags.append(tag)
    
    def __repr__(self):
        return '<Post id: {}, title {}>'.format(self.id, self.title)
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    link = db.Column(db.String(100))
    
    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.link = self.name.replace(' ', '-')
        
    def __repr__(self):
        return '<Tag id: {}, name {}>'.format(self.id, self.name)
        
    
    

        
    
    
        
        