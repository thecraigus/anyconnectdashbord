from netmiko import Netmiko
from netmiko import NetMikoTimeoutException
from asaanyconnectdashbord.models import gateway
import json
import csv
import os
import sys
import getopt

class ASA():

    def __init__(self,target,username,password):

        self.target = target
        self.username = username
        self.password = password


    def profileSSH(self):

        output = {}
        try:
            net_connect = Netmiko(host=self.target,username=self.username,password=self.password,device_type='cisco_asa')
            net_connect.find_prompt()
            neighbors = net_connect.send_command('show vpn-sessiondb',use_textfsm=True)
            hostname = net_connect.send_command('show hostname')

            output['currentsessions']  = neighbors[0]['anyconnect_client_active']

            net_connect.disconnect()
            # if isinstance(neighbors,list):
            #     output['SystemName'] = hostname.strip().split('.')[0]
            #     output['NeighborCount'] = len(neighbors)
            #     output['Neighbors'] = neighbors
            
            # else:
            #     output['SystemName'] = hostname.strip().split('.')[0]
            #     output['NeighborCount'] = 0
            #     output['Neighbors'] = None
            



            return output
        except NetMikoTimeoutException:
            return 'A timeout exception occured'
    

def environment_profile():
    pass
    # gateways = gateway.query.all()
    # gateway = ASA('192.168.254.200','craig','craig')
    # print (gateway.profileSSH())





# #### Runner #####
# if __name__ == '__main__':
#         environment_profile()
