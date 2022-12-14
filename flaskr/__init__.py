from flask import Flask, render_template
from .config import Config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)

    from .src import editor
    from .src import button
    from .src import scode
    app.register_blueprint(editor)
    app.register_blueprint(button)
    app.register_blueprint(scode)   

    @app.route("/about", methods = ['GET'])
    def setCode():
        return render_template('about.html') 

    @app.route('/')
    def home():
        return 'Home Page Route'  

    @app.errorhandler(404)
    def invalid_route(e): 
        return render_template('404.html')

    return app