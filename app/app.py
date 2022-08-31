from flask import Flask # импортируем фласк

from flask_login import LoginManager # импортируем loginmanager для соедение app

from flask_sqlalchemy import SQLAlchemy #импортируем SQLAlchemy для привязки бд к Flask

from config import Configuration #импортируем все конфиги

from flask_migrate import Migrate #Импортируем миграцию


#!Файл со всеми основными установками!#


app = Flask(__name__) #передаем app значение ФЛАСК#

app.config.from_object(Configuration) #передаем все конфиги в наше приложение app
 

db = SQLAlchemy(app) #создаем переменную которая будет являться нашей бд


login_manager = LoginManager() #создаем переменную
login_manager.login_view = 'login'
login_manager.login_message = "Авторизируйтесь для входа на эту страницу"
login_manager.init_app(app) #привязываю переменную с фласком 


from models import * #импортирую таблицы созданные в бд
migrate = Migrate(app, db) #создаю миграцию для базы данных



icons_location = 'app/static/icons'

