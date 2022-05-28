from distutils.command.config import config


class DevelopmentConfig():
    # Modo desarrollo - actualizaciones automaticas en el server
    DEBUG = True;
    #Detalle conexion a la bd
    MYSQL_DATABASE_HOST = 'localhost';
    MYSQL_DATABASE_USER = 'root';
    MYSQL_DATABASE_PASSWORD = 'admin@2022$';
    MYSQL_DATABASE_DB = 'api_flask';

config = {
    'development': DevelopmentConfig
}