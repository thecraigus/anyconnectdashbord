import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)



basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'sqlite.data')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

Migrate(app,db)

from asaanyconnectdashbord.gateways.views import gateways
from asaanyconnectdashbord.core.views import core

app.register_blueprint(gateways,url_prefix='/gateways')
app.register_blueprint(core,url_prefix='/')