# RUNNING THE APP:
# 
# First things first, activate the enviroment ('python3 -m venv venv' to create it while on top directory):
# . venv/bin/activate
#
# Terminal in top directory (flask_tutorial) in BASH:
#
# export FLASK_APP=flaskr
# export FLASK_ENV=development
# flask run


import os

from flask import Flask


def create_app(test_config=None):
    # we are creating and configuring the app here
    app = Flask(__name__, instance_relative_config=True)
    # this creates the flask instance
    # __name__ is the name of the current Python module. The app needs to know where it’s located to set up some paths
    # instance_... tells the app that configuration files are relative to the instance folder
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

