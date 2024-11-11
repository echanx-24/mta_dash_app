from flask_app.dashboard import create_dash
from flask import Flask, redirect

def create_app():
    app = Flask(__name__)

    plotly_dash = create_dash(app)

    @app.route("/dashboard")
    @app.route("/dashboard/")
    def dash_app():
        return redirect("/dashboard/")
    
    return app