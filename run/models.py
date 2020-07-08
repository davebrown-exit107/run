# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

from datetime import date, datetime

from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from run import db, ureg, Q_, login_manager
from run.lib import timestamp_to_datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_on = datetime.now()
        self.last_login = datetime.now()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    timestamp = db.Column(db.DateTime, nullable=False)

    elevation = db.Column(db.Numeric)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    distance = db.Column(db.Numeric)
    speed = db.Column(db.Numeric)

#    precipitation = db.Column(db.Numeric)
#    precipitation_type = db.Column(db.String)
#    temperature = db.Column(db.Numeric)
#    wind_bearing = db.Column(db.Numeric)
#    wind_speed = db.Column(db.Numeric)

    leg_id = db.Column(db.Integer, db.ForeignKey('leg.id'))
    leg = db.relationship('Leg', backref=db.backref('points'))

    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    run = db.relationship('Run', backref=db.backref('points'))

    @property
    def pace(self):
        speed = Q_(self.speed, ureg.kilometer_per_hour)
        pace = 60 / speed.to(ureg.mile_per_hour).magnitude
        return f"{round(pace):02}:{round((pace % 1) * 60):02}"

    @property
    def speed_in_mph(self):
        speed = Q_(self.speed, ureg.kilometer_per_hour)
        return speed.to(ureg.mile_per_hour).magnitude

    @property
    def distance_in_miles(self):
        distance = Q_(self.distance, ureg.meter)
        return distance.to(ureg.mile).magnitude

    @property
    def elevation_in_feet(self):
        elevation = Q_(self.elevation, ureg.meter)
        return elevation.to(ureg.foot).magnitude

    #TODO: Move lat long into one var: coords
    def __init__(self, timestamp, elevation, latitude,
                 longitude, distance, speed, leg, run):
        # Convert to datetime
        self.timestamp = timestamp_to_datetime(timestamp)
        self.elevation = elevation
        self.latitude = latitude
        self.longitude = longitude
        self.distance = distance
        self.speed = speed
#        self.precipitation = precipitation
#        self.precipitation_type = precipitation_type
#        self.temperature = temperature
#        self.wind_bearing = wind_bearing
#        self.wind_speed = wind_speed
        self.leg = leg
        self.run = run


class Leg(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Dynamic Properties
#    total_ascent = db.Column(db.Numeric(scale=1))
#    total_descent = db.Column(db.Numeric(scale=1))

    @property
    def centroid(self):
        latitude = db.session.query(func.avg(Point.latitude)).filter(Point.run_id == self.id).scalar()
        longitude = db.session.query(func.avg(Point.longitude)).filter(Point.run_id == self.id).scalar()
        return {
            'latitude': latitude,
            'longitude': longitude
        }

    @property
    def avg_pace(self):
        avg_speed = db.session.query(func.avg(Point.speed)).filter(Point.leg_id == self.id).scalar()
        pace = 60 / Q_(avg_speed, ureg.kilometer_per_hour).to(ureg.mile_per_hour).magnitude
        return f"{round(pace):02}:{round((pace % 1) * 60):02}"

    @property
    def max_pace(self):
        avg_speed = db.session.query(func.max(Point.speed)).filter(Point.leg_id == self.id).scalar()
        pace = 60 / Q_(avg_speed, ureg.kilometer_per_hour).to(ureg.mile_per_hour).magnitude
        return f"{round(pace):02}:{round((pace % 1) * 60):02}"

    @property
    def avg_speed(self):
        return db.session.query(func.avg(Point.speed)).filter(Point.leg_id == self.id).scalar()

    @property
    def max_speed(self):
        return db.session.query(func.max(Point.speed)).filter(Point.leg_id == self.id).scalar()

    @property
    def start_datetime(self):
        return self.points[0].timestamp

    @property
    def end_datetime(self):
        return self.points[-1].timestamp

    @property
    def distance(self):
        return self.points[-1].distance - self.points[0].distance

    @property
    def distance_in_miles(self):
        distance = Q_(self.distance, ureg.meter)
        return distance.to(ureg.mile).magnitude

    @property
    def start_position(self):
        return {
            'longitude': self.points[0].longitude,
            'latitude': self.points[0].latitude
        }

    @property
    def end_position(self):
        return {
            'longitude': self.points[-1].longitude,
            'latitude': self.points[-1].latitude
        }

    total_timer_time = db.Column(db.Numeric(scale=2))
    total_elapsed_time = db.Column(db.Numeric(scale=2))

    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    run = db.relationship('Run', backref=db.backref('legs'))

    def __init__(self, run):
        self.run = run


class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    start_time = db.Column(db.DateTime)
    total_timer_time = db.Column(db.Numeric(scale=2))
    total_elapsed_time = db.Column(db.Numeric(scale=2))

    # Dynamic Properties
#    total_ascent = db.Column(db.Numeric(scale=1))
#    total_descent = db.Column(db.Numeric(scale=1))

    @property
    def centroid(self):
        latitude = db.session.query(func.avg(Point.latitude)).filter(Point.run_id == self.id).scalar()
        longitude = db.session.query(func.avg(Point.longitude)).filter(Point.run_id == self.id).scalar()
        print(latitude)
        print(longitude)
        return {
            'latitude': latitude,
            'longitude': longitude
        }

    @property
    def avg_pace(self):
        avg_speed = db.session.query(func.avg(Point.speed)).filter(Point.run_id == self.id).scalar()
        pace = 60 / Q_(avg_speed, ureg.kilometer_per_hour).to(ureg.mile_per_hour).magnitude
        return f"{round(pace):02}:{round((pace % 1) * 60):02}"

    @property
    def max_pace(self):
        avg_speed = db.session.query(func.max(Point.speed)).filter(Point.run_id == self.id).scalar()
        pace = 60 / Q_(avg_speed, ureg.kilometer_per_hour).to(ureg.mile_per_hour).magnitude
        return f"{round(pace):02}:{round((pace % 1) * 60):02}"

    @property
    def avg_speed(self):
        return db.session.query(func.avg(Point.speed)).filter(Point.run_id == self.id).scalar()

    @property
    def max_speed(self):
        return db.session.query(func.max(Point.speed)).filter(Point.run_id == self.id).scalar()

    @property
    def start_position(self):
        return {
            'longitude': self.points[0].longitude,
            'latitude': self.points[0].latitude
        }

    @property
    def end_position(self):
        return {
            'longitude': self.points[-1].longitude,
            'latitude': self.points[-1].latitude
        }

    @property
    def start_datetime(self):
        return self.points[0].timestamp

    @property
    def end_datetime(self):
        return self.points[-1].timestamp

    @property
    def distance(self):
        return self.points[-1].distance

    @property
    def distance_in_miles(self):
        distance = Q_(self.distance, ureg.meter)
        return distance.to(ureg.mile).magnitude

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('runs'))

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City', backref=db.backref('runs'))

    def __init__(self, city, user):
        self.city = city
        self.user = user


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    state = db.relationship('State', backref=db.backref('cities'))

    def __init__(self, name, state):
        self.name = name
        self.state = state


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', backref=db.backref('states'))

    def __init__(self, name, country):
        self.name = name
        self.country = country


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

