from sqlalchemy.orm import column_property
from sqlalchemy import select, func

from run import db
from run.lib import *

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

#    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
#    run = db.relationship('Run', backref=db.backref('points'))

#    speed_mph = lambda x: round(x*2.236936,2)
#    dist_miles = lambda x: round(x*0.00062137,2)
#    elevation_feet = lambda x: round(x*3.281)

    def __init__(self, timestamp, elevation, latitude, 
                  longitude, distance, speed, leg):
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
#        self.run = run


class Leg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avg_speed = db.Column(db.Numeric(scale=3))
    max_speed = db.Column(db.Numeric(scale=3))

    start_position_lat = db.Column(db.Float)
    start_position_long = db.Column(db.Float)
    end_position_lat = db.Column(db.Float)
    end_position_long = db.Column(db.Float)

    # Dynamic Properties
#    total_ascent = db.Column(db.Numeric(scale=1))
#    total_descent = db.Column(db.Numeric(scale=1))
#    total_distance = db.Column(db.Numeric(scale=2))

#    timestamp = db.Column(db.String)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)

    total_timer_time = db.Column(db.Numeric(scale=2))
    total_elapsed_time = db.Column(db.Numeric(scale=2))

    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    run = db.relationship('Run', backref=db.backref('legs'))


    def __init__(self, start_position_lat, start_position_long, 
                end_position_lat, end_position_long, start_datetime,
                end_datetime, total_timer_time, total_elapsed_time, run):
        #self.avg_speed = avg_speed
        #self.max_speed = max_speed
        self.start_position_lat = start_position_lat
        self.start_position_lng = start_position_lng
        self.end_position_lat = end_position_lat
        self.end_position_lng = end_position_lng
        #self.total_ascent = total_ascent
        #self.total_descent = total_descent
        #self.total_distance = total_distance
        self.start_datetime = pendulum.instance(start_datetime)
        self.end_datetime = pendulum.instance(end_datetime)
        self.total_timer_time = total_timer_time
        self.total_elapsed_time = total_elapsed_time
        self.run = run


class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#    avg_speed = db.Column(db.Numeric(scale=3))
#    max_speed = db.Column(db.Numeric(scale=3))

    start_position_lat = db.Column(db.Float)
    start_position_long = db.Column(db.Float)
    end_position_lat = db.Column(db.Float)
    end_position_long = db.Column(db.Float)
#    total_ascent = db.Column(db.Numeric(scale=1))
#    total_descent = db.Column(db.Numeric(scale=1))
#    total_distance = db.Column(db.Numeric(scale=2))

    start_time = db.Column(db.DateTime)
    total_timer_time = db.Column(db.Numeric(scale=2))
    total_elapsed_time = db.Column(db.Numeric(scale=2))

#    race_overall_place = db.Column(db.String)
#    race_age_group = db.Column(db.String)
#    race_age_group_place = db.Column(db.String)
#    race_chip_time = db.Column(db.Numeric)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city = db.relationship('City', backref=db.backref('runs'))
#    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
#    state = db.relationship('State', backref=db.backref('runs'))
#    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
#    country = db.relationship('Country', backref=db.backref('runs'))
#    timezone_id = db.Column(db.Integer, db.ForeignKey('timezone.id'))
#    timezone = db.relationship('Timezone', backref=db.backref('runs'))
#    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
#    race = db.relationship('Race', backref=db.backref('runs'))

    def __init__(self, start_position_lat, start_position_long,
                  end_position_lat, end_position_long, start_time,
                  total_timer_time, total_elapsed_time, city):
        self.start_position_lat = start_position_lat
        self.start_position_lng = start_position_lng
        self.end_position_lat = end_position_lat
        self.end_position_lng = end_position_lng
        #self.total_ascent = total_ascent
        #self.total_descent = total_descent
        #self.total_distance = total_distance
        self.start_time = timestamp_to_datetime(start_time)
        self.total_timer_time = total_timer_time
        self.total_elapsed_time = total_elapsed_time
        #self.day = day
        self.city = city
        #self.state = state
        #self.country = country
        #self.timezone = timezone


#class Day(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    sunrise = db.Column(db.DateTime)
#    sunset = db.Column(db.DateTime)
#    date = db.Column(db.Date)
#
#    def __init__(self, date):
#        self.date = date
#
# I feel like city should have a mapping to state which should have a mapping to country
# this way we could only need to specify a city in the run and everything else would be
# taken care of. This would also make relationships a bit easier.

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    state = db.relationship('State', backref=db.backref('cities'))

    def __init__(self, name):
        self.name = name

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship('Country', backref=db.backref('states'))

    def __init__(self, name):
        self.name = name

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

#class Timezone(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String)
#
#    def __init__(self, name):
#        self.name = name
#
#class Race(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String, unique=True)
#
##    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
##    city = db.relationship('City', backref=db.backref('runs'))
##    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
##    state = db.relationship('State', backref=db.backref('runs'))
##    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
##    country = db.relationship('Country', backref=db.backref('runs'))
#
#    #def __init__(self, name, city, state, country):
#    def __init__(self, name):
#        self.name = name
##        self.city = city
##        self.state = state
##        self.country = country