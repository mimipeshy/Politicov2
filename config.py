import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = "sijuiaki"


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    TESTING = True



class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_NAME = "test_andela"


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {'development': DevelopmentConfig,
              'testing': TestingConfig,
              'production': ProductionConfig,
              'default': DevelopmentConfig

              }
