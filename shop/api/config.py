import os


class Config(object):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGOALCHEMY_DATABASE = 'imse_mongo_db'
    MONGOALCHEMY_SERVER = 'mongodb'
    MONGOALCHEMY_PORT = 27017
    # MONGOALCHEMY_USER = 'user'
    # MONGOALCHEMY_PASSWORD = 'password'
    # MONGOALCHEMY_CONNECTION_STRING = 'mongodb://user:password@mongodb:27017/imse_mongo_db?authSource=admin'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # used to encrypt user's passwords
    TEMPLATES_FOLDER = os.environ.get('TEMPLATES_FOLDER')
    JWT_SECRET_KEY = 'you-will-never-guess'
