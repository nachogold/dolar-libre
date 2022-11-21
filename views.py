#TO DO:
#AUTOMATIZAR PROCESO DE GET DATA : https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
from flask import Blueprint, render_template
from modules.get_data import get_data

views = Blueprint(__name__,"views")

df = get_data()

@views.route("/")
def home():
    return render_template("base.html",df=df)