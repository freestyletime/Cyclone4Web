import os, sys
from flaskr import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

app = create_app()


# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0")

if __name__ == "__main__":
    app.run(port=8080)