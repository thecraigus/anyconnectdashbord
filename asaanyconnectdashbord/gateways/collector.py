from netmiko import Netmiko
from netmiko import NetMikoTimeoutException
from asaanyconnectdashbord.models import gateway
from asaanyconnectdashbord.models import db
import os
from time import sleep

templatespath = os.path.join( os.path.dirname( __file__ ), 'textfsm/templates' )
os.environ['NET_TEXTFSM'] = templatespath


def gatewayconnect(target,username,password):
    try:
        net_connect = Netmiko(host=target,username=username,password=password,device_type='cisco_asa', timeout=3)
        net_connect.find_prompt()
    except:
        net_connect = False

    return net_connect

def getcurrentuserdata(net_connect):
    try:
        data = net_connect.send_command('show vpn-sessiondb',use_textfsm=True)
    except:
        data = [{'anyconnect_client_active':'0'}]
    # net_connect.disconnect()
    return data

def getcurrentusers(data):
    anyconnectusers = data[0]['anyconnect_client_active']
    return anyconnectusers

def getvpnlicenceuseage(data,currentusers):
    permiumpeers = data[0]['premium_peers']
    totalvpnpeers = data[0]['total_vpn_peers']
    anyconnectessentials = data[0]['anyconnect_essentials']

    if anyconnectessentials != 'Disabled':
        totalpool = int(permiumpeers) + int(totalvpnpeers)
    else:
        totalpool = int(permiumpeers)
    
    percentageuseage = int(currentusers) / int(totalpool) * 100
    percentagestring = str(percentageuseage).split('.')[0]+'%'

    return percentagestring



def writedata(target, users, status,licenceuseage):
    target.currentusers = users
    target.gwstatus = status
    target.vpnlicenseusage = licenceuseage
    db.session.commit()

def getvpnlicencedata(net_connect):
    data = net_connect.send_command('show version', use_textfsm=True)
    return data 


def main():
    onlinestatus = 'Online'
    offlinestatus = 'Unreachable'
    targets = gateway.query.all()
    for target in targets:
        connection = gatewayconnect(target.ipv4addr, target.sshuser, target.sshpass)
        if connection:
            data = getcurrentuserdata(connection)
            users = getcurrentusers(data)
            licencedata = getvpnlicencedata(connection)
            licenceuseage = getvpnlicenceuseage(licencedata,users)
            connection.disconnect()
            sleep(3)
            writedata(target,users,onlinestatus,licenceuseage)
        else:
            writedata(target,0,offlinestatus,'0%')