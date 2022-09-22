import os

class Config:
    SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
    SECRET_KEY = os.environ.get("SECRET_KEY")
