# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from flask import Flask
from flask_login import LoginManager
#from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pint import UnitRegistry


##################################################
# Setup unit conversions for the application
##################################################
ureg = UnitRegistry()
Q_ = ureg.Quantity

##################################################
# Initialze and Configure Application
##################################################
run_app = Flask(__name__)
run_app.config.from_pyfile('../config/run_app.conf')

##################################################
# SQLAlchemy setup
##################################################
db = SQLAlchemy(run_app)

##################################################
# flask-migrate setup
##################################################
migrate = Migrate(run_app, db)

###################################################
## flask-login setup
###################################################
login_manager = LoginManager(run_app)
login_manager.login_view = 'login'

###################################################
## flask-admin setup
###################################################
#admin = Admin()
#admin.init_app(run_app)

# Import routes
##################################################
from run import routes
