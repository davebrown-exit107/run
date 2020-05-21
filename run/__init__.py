# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from flask import Flask
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
run_app.config.from_pyfile('config/run_app.conf')

##################################################
# SQLAlchemy setup
##################################################
db = SQLAlchemy(run_app)

migrate = Migrate(run_app, db)
##################################################
# Import routes
##################################################
from run import routes
