# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from flask import render_template

from run import db
from run import run_app
# from run.models import Country, State, City, Run, Leg, Point
from run.models import Run, Leg, Point


##################################################
# Frontends
##################################################
@run_app.route('/', methods=['GET'])
def landing_page():
    return 'landing_page'


@run_app.route('/point/', methods=['GET'])
def list_points():
    points = db.session.query(Point).all()
    return render_template('list_points.html.j2', points=points)


@run_app.route('/run/', methods=['GET'])
def list_runs():
    runs = db.session.query(Run).all()
    return render_template('list_runs.html.j2', runs=runs)


@run_app.route('/leg/', methods=['GET'])
def list_legs():
    legs = db.session.query(Leg).all()
    return render_template('list_legs.html.j2', legs=legs)


@run_app.route('/leg/<int:leg_id>', methods=['GET'])
def detail_leg(leg_id):
    leg = db.session.query(Leg).get_or_404(leg_id)
    return render_template('detail_leg.html.j2', leg=leg, MAPBOX_API_KEY=run_app.config['MAPBOX_API_KEY'])

@run_app.route('/run/<int:run_id>', methods=['GET'])
def detail_run(run_id):
    run = db.session.query(Run).get_or_404(run_id)
    return render_template('detail_run.html.j2', run=run, MAPBOX_API_KEY=run_app.config['MAPBOX_API_KEY'])
