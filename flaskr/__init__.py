from flask import Flask, redirect, render_template
from .config import Config, const

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)

    # use Blueprint to make the project structure flexible
    from .src import editor
    app.register_blueprint(editor)  

    @app.route("/about", methods = ['GET'])
    def about():
        """
        Introduce the author and the techs of the website
        ---
        description: show users the webpage 'about.html'
        parameters:
        responses:
        200:
            description: successfully show the webpage 'about.html'
        """

        return render_template('about.html') 

    @app.route('/', methods = ['GET'])
    def home():
        """
        Homepage
        ---
        description: show users webpage 'index.html'
        parameters:
        responses:
        200:
            description: successfully redirect to the webpage 'index.html'
        """

        return redirect("/editor", code=302)

    @app.errorhandler(404)
    def page_404(e):
        """
        404 webpage
        ---
        description: show users webpage 'error.html'
        responses:
        200:
            description: successfully show the webpage 'error.html'
        """

        return render_template(const.HTML_ERROR, code=404, des=const.DES_HTTP_CODE_404)

    @app.errorhandler(405)
    def page_403(e):
        """
        405 webpage
        ---
        description: show users webpage 'error.html'
        responses:
        200:
            description: successfully show the webpage 'error.html'
        """

        return render_template(const.HTML_ERROR, code=405, des=const.DES_HTTP_CODE_405)

    return app