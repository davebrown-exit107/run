from flask import request, session, abort, render_template, \
    send_file, jsonify, json, url_for, flash, redirect

#from datetime import date, datetime, timedelta
#import dateutil.parser
#from io import BytesIO
#from itertools import groupby
#import tablib
#from decimal import *
#from sqlalchemy import desc
#from sqlalchemy.orm import exc
#from StringIO import StringIO
#import xlrd

from run import db
from run import run_app
from run.models import Timezone, Country, State, City, Day, Run, Race

##################################################
# Frontends
##################################################
@run_app.route('/', methods=['GET'])
def landing_page():
  return 'landing_page'

@run_app.route('/list', methods=['GET'])
def run_list():
  return 'list of runs'
