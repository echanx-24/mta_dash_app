from flask import Blueprint, redirect

main = Blueprint("main", __name__)

@main.route("/dashboard")
@main.route("/dashboard/")
def dash_app():
    return redirect("/dashboard/")