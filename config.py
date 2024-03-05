class Config:
    SECRET_KEY = 'wazxdesz21'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024