from flask import Blueprint,render_template,redirect,url_for
from asaanyconnectdashbord import db
from asaanyconnectdashbord.models import gateway
from asaanyconnectdashbord.gateways.forms import AddGateway, DelGateway


gateways = Blueprint('gateways',__name__, template_folder='templates/gateways')

@gateways.route('/add',methods=['GET','POST'])
def add():

    form = AddGateway()

    if form.validate_on_submit():
        name = form.gatewayname.data
        ipv4addr = form.ipv4addr.data
        user = form.sshuser.data
        password = form.sshpassword.data
        newgateway = gateway(name,ipv4addr,user,password)
        db.session.add(newgateway)
        db.session.commit()

        return redirect(url_for('gateways.list_gateways'))
    
    return render_template('addgateway.html',form=form)

@gateways.route('/list')
def list_gateways():
    gateways = gateway.query.all()
    return render_template('listgateway.html',gateways=gateways)

@gateways.route('/delete',methods=['GET','POST'])
def del_gateway():

    form = DelGateway()

    if form.validate_on_submit():
        id = form.gatewayid.data
        fordelete = gateway.query.get(id)
        db.session.delete(fordelete)
        db.session.commit()

     
        return redirect(url_for('gateways.list_gateways'))
    
    return render_template('deletegateway.html', form=form)