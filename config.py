import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    TESTING = True
    JWT_SECRET_KEY = "sijuiaki"


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_NAME = "testpolitico"
    JWT_SECRET_KEY = "sijuiaki"


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = "sijuiaki"


app_config = {'development': DevelopmentConfig,
              'testing': TestingConfig,
              'production': ProductionConfig,
              'default': DevelopmentConfig

              }
