from flask_app.dashboard import create_dash
from flask_app.main.routes import main
from flask import Flask

def create_app():
    app = Flask(__name__)

    plotly_dash = create_dash(app)

    app.register_blueprint(main)
    
    return app