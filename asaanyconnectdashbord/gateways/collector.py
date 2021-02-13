from netmiko import Netmiko
from netmiko import NetMikoTimeoutException
from asaanyconnectdashbord.models import gateway
from asaanyconnectdashbord.models import db

def gatewayconnect(target,username,password):
    try:
        net_connect = Netmiko(host=target,username=username,password=password,device_type='cisco_asa', timeout=3)
        net_connect.find_prompt()
    except:
        net_connect = False

    return net_connect

def getdata(net_connect, command):
    try:
        data = net_connect.send_command(command,use_textfsm=True)
    except:
        data = [{'anyconnect_client_active':'0'}]
    net_connect.disconnect()
    return data

def getcurrentusers(data):
    anyconnectusers = data[0]['anyconnect_client_active']
    return anyconnectusers

def writedata(target, users, status):
    target.currentusers = users
    target.gwstatus = status
    db.session.commit()


def main():
    onlinestatus = 'Online'
    offlinestatus = 'Unreachable'
    command = 'show vpn-sessiondb'
    targets = gateway.query.all()
    for target in targets:
        connection = gatewayconnect(target.ipv4addr, target.sshuser, target.sshpass)
        if connection:
            data = getdata(connection, command)
            users = getcurrentusers(data)
            writedata(target,users,onlinestatus)
        else:
            writedata(target,0,offlinestatus)