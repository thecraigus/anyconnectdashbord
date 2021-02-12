from flask import Blueprint,render_template,redirect,url_for
from asaanyconnectdashbord import db
from asaanyconnectdashbord.models import gateway


core = Blueprint('core',__name__, template_folder='templates/core')

@core.route('/',methods=['GET','POST'])
def home():
    gateways = gateway.query.all()
    return render_template('home.html', gateways=gateways)

