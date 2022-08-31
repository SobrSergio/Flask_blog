from app import app #импортируем приложение фласк для его запуска

from app import db #импортирую бд

from routes import * #импортируем все адреса для нашего сайта (@app.route)

#!Файл для запуска Flask!#


if __name__ == '__main__':  #Формула для запуска веб-приложения
    app.run()