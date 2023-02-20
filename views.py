from flask import Blueprint, render_template
from modules.get_data import get_data
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import atexit

views = Blueprint(__name__,"views")

#scrape data and save it to csv
def update_data():
    print('updating data')
    data = get_data()
    data.to_csv('data.csv',index=False)

#call function first time
update_data()

#schedule function to have fresh data every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data, trigger="interval", minutes=10)
scheduler.start()

@views.route("/")
def home():
    return render_template("index.html",df=pd.read_csv('data.csv'))

atexit.register(lambda: scheduler.shutdown())
