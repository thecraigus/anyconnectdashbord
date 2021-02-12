from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, IPAddress
from wtforms import ValidationError
from asaanyconnectdashbord.models import gateway

class AddGateway(FlaskForm):

    gatewayname  = StringField('Gateway Name: ',validators=[DataRequired()])
    ipv4addr = StringField('Gateway IPv4 Address: ', validators=[DataRequired(), IPAddress()])
    sshuser = StringField('Gateway SSH Username: ', validators=[DataRequired()])
    sshpassword = PasswordField('SSH User Password: ',validators=[DataRequired(),EqualTo('confirmpassword', message='Please ensure passwords match')])
    confirmpassword = PasswordField('Confirm SSH User Password', validators=[DataRequired()])
    submit = SubmitField('Add Gateway')

    def validate_ipv4addr(self,field):
        if gateway.query.filter_by(ipv4addr=self.ipv4addr.data).first():
            raise ValidationError(message='This IPv4 Address Is Already Being Monitored')

    def validate_gatewayname(self,field):
        if gateway.query.filter_by(gatewayname=self.gatewayname.data).first():
            raise ValidationError(message='This Gateway Name Is Already In Use')

class DelGateway(FlaskForm):
    gatewayid = StringField('Gateway You Wish To Remove: ')
    submit  = SubmitField('Remove Gateway')

    def check_gatewayid(self,field):
        if not gateway.query.filter_by(id=self.data()).first():
            raise ValidationError(message='This Gateway Is Not Recognised')


