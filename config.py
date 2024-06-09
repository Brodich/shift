import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    JWT_EXPIRATION_DELTA = 10  # minutes
