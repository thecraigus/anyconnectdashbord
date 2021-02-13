from netmiko import Netmiko
from netmiko import NetMikoTimeoutException
import os 


templatespath = os.path.join( os.path.dirname( __file__ ), 'textfsm/templates' )
os.environ['NET_TEXTFSM'] = templatespath


net_connect = Netmiko(host='192.168.254.200',username='craig',password='craig',device_type='cisco_asa', timeout=3)
net_connect.find_prompt()

data = net_connect.send_command('show version',use_textfsm=True)

print (data)