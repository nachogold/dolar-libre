from flask import Blueprint, render_template
from modules.get_data import get_data
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import atexit

views = Blueprint(__name__,"views")

#definimos funcion para scrapear data y guardarla en un csv. De acá vamos a tomar la data para mostrar en el html
def update_data():
    print('updating data')
    data = get_data()
    data.to_csv('dolar-libre/data.csv',index=False)

#corremos por primera vez la funcion
update_data()

#scheduleamos la funcion para tener data nueva cada 10 minutos
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data, trigger="interval", minutes=10)
scheduler.start()

@views.route("/")
def home():
    return render_template("index.html",df=pd.read_csv('dolar-libre/data.csv'))

atexit.register(lambda: scheduler.shutdown())