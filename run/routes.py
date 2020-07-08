# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

##########################################
# 3rd party modules
###########################################
from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

###########################################
# import application components
############################################
from run import db
from run import run_app
from run.forms import LoginForm
from run.lib import parse_file
from run.models import Leg, Point, Run, User

##################################################
# Landing Page
##################################################
@run_app.route('/', methods=['GET'])
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html.j2', current_user=current_user)
    return redirect(url_for('login'))

##################################################
# Auth/User
##################################################
@run_app.route('/profile', methods=['GET'])
def profile():
    return 'profile'

@run_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html.j2', title='Sign In', form=form)

@run_app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@run_app.route('/signup', methods=['GET', 'POST'])
def signup():
    return 'Not available yet'


##################################################
# Frontends
##################################################
@run_app.route('/point/', methods=['GET'])
@login_required
def list_points():
    points = db.session.query(Point).all()
    return render_template('list_points.html.j2', points=points)


@run_app.route('/run/', methods=['GET'])
@login_required
def list_runs():
    runs = current_user.runs
    return render_template('list_runs.html.j2', runs=runs)


@run_app.route('/leg/', methods=['GET'])
@login_required
def list_legs():
    legs = db.session.query(Leg).all()
    return render_template('list_legs.html.j2', legs=legs)


@run_app.route('/leg/<int:leg_id>', methods=['GET'])
@login_required
def detail_leg(leg_id):
    leg = db.session.query(Leg).get_or_404(leg_id)
    return render_template('detail_leg.html.j2',
                           leg=leg,
                           MAPBOX_API_KEY=run_app.config['MAPBOX_API_KEY'])

@run_app.route('/run/<int:run_id>', methods=['GET'])
@login_required
def detail_run(run_id):
    run = db.session.query(Run).get_or_404(run_id)
    return render_template('detail_run.html.j2',
                           run=run,
                           MAPBOX_API_KEY=run_app.config['MAPBOX_API_KEY'])

##################################################
# Backends
##################################################
@run_app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'fit_file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        fit_file = request.files['fit_file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if fit_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if fit_file:
            run_id = parse_file(db, fit_file.stream, current_user)
            return redirect(url_for('detail_run', run_id=run_id))
    return render_template('upload.html.j2')
