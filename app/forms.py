from flask_wtf import FlaskForm #импортирую главный класс для Forms

from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo #импортирую валидаторы для проверки введеной информации
                                                                                                        # 1)  DataRequired - нужно внести хотя-бы один символ!
                                                                                                        # 2)  Length - проверяет количество введенных символов
                                                                                                        # 3)  ValidationError - Возникает, когда валидатор не может проверить свой ввод
                                                                                                        # 4)  Email - Проверяет адрес электронной почты. Требуется наличие пакета email_validator
                                                                                                        # 5)  EqualTo - Сравнивает значения двух полей    
from wtforms import BooleanField, PasswordField, SubmitField, TextAreaField, StringField, FileField #импортирую разные поля ввода

from models import * #импортирую все таблицы из бд


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Войти')
    remember_me = BooleanField('Запомнить меня')
    
    def validate_username(self, username): #validation_on_submit даст проверку на это, что проверит имя пользователя и пароль 
        user = User.query.filter_by(username = username.data).first() #проверка сущетсвует ли такой пользователь
        if (user is None) or (not user.check_password(self.password.data)): #если пользователя нет или пароль не совпадает то ошибка.
            raise ValidationError('Введите правильное имя пользователя или пароль')
        
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Слишком короткий или длинный логин')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неверный формат почты')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80, message='Слишком короткий или длинный пароль')])
    password_r = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80, message='Слишком короткий или длинный пароль'), EqualTo('password', message='Повторный пароль неправильный')]) #повторный пароль 
    submit = SubmitField('Зарегистрироваться')
    
    photo = FileField()
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #проверка, что если такой email существует то выводит ошибку 
        if user is not None:
            raise ValidationError('Такой email уже зарегистрирован')
        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #проверка, что если такой пользователь существует то выводит ошибку 
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

class Profileform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Слишком короткий или длинный логин')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Неверный формат почты')])
    photo = FileField() #аватарка для пользователя
    
    first_name = StringField(validators=[Length(min=3, max=25, message='Слишком короткое или длинное имя')])
    last_name = StringField(validators=[Length(min=3, max=25, message='Слишком короткая или длинная фамилия')])
    age = StringField()
    location = StringField(validators=[Length(min=3, max=20, message='Сликом короткое или длинное название города')])

    submit = SubmitField('Сохранить')

class CreateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=3, max=30, message='Слишком короткое или длинное название')])
    body = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Создать')


class EditPostForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=3, max=30, message='Слишком короткое или длинное название')])
    body = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Изменить')