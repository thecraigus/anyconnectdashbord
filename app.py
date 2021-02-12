from asaanyconnectdashbord import app
from flask import render_template
from flask_apscheduler import APScheduler
from netmiko import Netmiko
from netmiko import NetMikoTimeoutException
from asaanyconnectdashbord.models import gateway
from asaanyconnectdashbord.models import db


scheduler = APScheduler()

def fecthdata():
    targets = gateway.query.all()
    for x in targets:
        net_connect = Netmiko(host=x.ipv4addr,username=x.sshuser,password=x.sshpass,device_type='cisco_asa')
        net_connect.find_prompt()
        try:
            neighbors = net_connect.send_command('show vpn-sessiondb',use_textfsm=True)
            anyconnectusers = neighbors[0]['anyconnect_client_active']
            net_connect.disconnect()
            x.currentusers = int(anyconnectusers)
            db.session.commit()
        except:
            pass


@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    scheduler.add_job(id='anyconnectprofile', func=fecthdata, trigger='interval', seconds=60)
    scheduler.start()
    app.run(debug=True)
    