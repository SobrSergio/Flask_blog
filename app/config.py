class Configuration():  #создаем класс в котором будут все config для нашего app (фласка)
    DEBUG = True #включаем дебагер.
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///my_sql.db' #передаем где будет создаваться база данных
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Запись что-бы не было надписи в консоли
        
    SECRET_KEY = 'HERE-VERY-COMPLEX-SECRET-KEY' #создание секретного ключа нужного для работы многих функций 
    
    