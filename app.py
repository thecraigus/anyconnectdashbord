from asaanyconnectdashbord import app
from flask import render_template
from flask_apscheduler import APScheduler
from netmiko import Netmiko
from netmiko import NetMikoTimeoutException
from asaanyconnectdashbord.models import gateway
from asaanyconnectdashbord.models import db
from asaanyconnectdashbord.gateways.collector import main


scheduler = APScheduler()


@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    scheduler.add_job(id='anyconnectprofile', func=main, trigger='interval', seconds=60)
    scheduler.start()
    app.run(debug=True)
    