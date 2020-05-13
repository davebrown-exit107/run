from flask import Flask
#from path import Path
import os

##################################################
# Initialze and Configure Application
##################################################
run_app = Flask(__name__)
#run_app.config.from_envvar('RUN_APP_CONFIG')
run_app.config.from_pyfile('config/run_app.conf')

##################################################
# SQLAlchemy setup
##################################################
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(run_app)

##################################################
# Routes
##################################################
from run import routes
