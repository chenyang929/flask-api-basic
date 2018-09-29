import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    TOKEN_EXPIRATION = 3600 * 24 * 7
    UPLOAD_FOLDER = os.path.join(basedir, 'upload')
    ALLOW_EXTENSIONS = set(['xlsx', 'xls'])

    @classmethod
    def init_app(cls, app):

        if not os.path.exists(cls.UPLOAD_FOLDER):
            os.makedirs(cls.UPLOAD_FOLDER)


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://coder:coder@localhost:27017/test'


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    TOKEN_EXPIRATION = 3600 * 2
    MONGO_URI = 'mongodb://coder:coder@localhost:27017/test'
    # 生成key
    # import os
    # os.urandom(24)
    SECRET_KEY = '\x10G\x0fjC\xe99\xc2\x02\xf1\xf6\xb4\xd82xJD\x9c\xc5x\xe6\xfa\xe8\xa6'


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

