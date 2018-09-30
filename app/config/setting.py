# 配置常量
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'hard to guess'
TOKEN_EXPIRATION = 3600 * 24 * 7
ALLOW_EXTENSIONS = set(['xlsx', 'xls'])
UPLOAD_FOLDER = os.path.join(basedir, 'upload')
MONGO_URI = "mongodb://localhost:27017/test"


