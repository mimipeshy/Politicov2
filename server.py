import os
from app.api.app import create_app


app = create_app(os.getenv('CONFIG_SETTING'))


if __name__ == '__main__':
    app.run()
8