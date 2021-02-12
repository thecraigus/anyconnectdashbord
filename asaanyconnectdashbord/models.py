from asaanyconnectdashbord import db
from werkzeug.security import generate_password_hash,check_password_hash

class gateway(db.Model):

    __tablename__ = 'gateway'

    id = db.Column(db.Integer, primary_key=True)
    gatewayname = db.Column(db.String(20))
    ipv4addr = db.Column(db.String(20))
    sshuser = db.Column(db.String(20))
    sshpass = db.Column(db.String(20))
    currentusers = db.Column(db.Integer,default=0)
    def __init__(self,gatewayname,ipv4addr,sshuser,sshpass):
        self.gatewayname = gatewayname
        self.ipv4addr = ipv4addr
        self.sshuser = sshuser
        self.sshpass = sshpass
        # self.currentusers = currentusers

    def __repr__(self):
        return f'Gateway Name: {self.gatewayname} IP: {self.ipv4addr}'



