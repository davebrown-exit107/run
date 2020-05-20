import sys
import os

##########################################
# 3rd party modules
###########################################
import click
import json
import pendulum
import requests

from fitparse import FitFile, FitParseError
from fitparse.processors import StandardUnitsDataProcessor, FitFileDataProcessor
from geopy.geocoders import OpenMapQuest
#from pint import UnitRegistry
from timezonefinder import TimezoneFinder

###########################################
# setup configuration and path for imports
############################################
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

###########################################
# import application components
############################################
from run import run_app
from run import db
from run.lib import *
from run.models import Country, State, City, Run, Leg, Point
from run import ureg, Q_

##########################################
# Open the file named on the command line
###########################################
@click.command()
@click.option('--debug/--no-debug', default=True)
@click.argument('fitfile_in', type=click.File('rb'))
def parse_run(debug, fitfile_in):
  print(debug)
  ##########################################
  # Parse the fit file
  ###########################################
  try:
    fitfile_processor = StandardUnitsDataProcessor()
    fitfile = FitFile(fitfile_in, data_processor=fitfile_processor, check_crc=False)
    fitfile.parse()
  except FitParseError as err:
    print('Error while parsing {}: {}'.format(fitfile_in.relpath(), err))
    sys.exit(1)

  # Build our api instances
  geocoder = OpenMapQuest(api_key=run_app.config['OPEN_MAPQUEST_KEY'], scheme='http', timeout=100)
  tf = TimezoneFinder()
  #ureg = UnitRegistry()

  # Pull manufacturer data
  for record in fitfile.get_messages('file_id', with_definitions=False): 
    manufacturer = record.get_value('manufacturer')
    product = record.get_value('garmin_product')

  for record in fitfile.get_messages('file_creator', with_definitions=False): 
    pass

  if debug:
    print(f"device: {manufacturer} -- {product}")
    print()

  # Parse all events
  for record in fitfile.get_messages('event', with_definitions=False): 
    event_group = record.get_value('event_group')
    timestamp = record.get_value('timestamp')
    if debug:
      print(f"event: {event_group} -- {timestamp}")
      for record_data in record: 
          print(f" * {record_data.name}: {record_data.value}")
      print()

  initial = True
  for record in fitfile.get_messages('record', with_definitions=False): 
    # Parse all fields
    lat = record.get_value('position_lat')
    lng = record.get_value('position_long')
    if lat and lng:
      timezone = find_timezone(tf,lat,lng)
      location = geocoder.reverse([lat,lng]).raw
    else:
      print('skipping record w/o lat or long\n')
      continue

    utc_time = pendulum.instance(record.get_value('timestamp'))
    local_tz = pendulum.timezone(timezone)
    local_time = local_tz.convert(utc_time)

    distance = record.get_value('distance') * ureg.km
    elevation = record.get_value('enhanced_altitude') * ureg.meter
    speed = record.get_value('enhanced_speed') * ureg.kilometer_per_hour
    if speed.magnitude > 0:
      pace = 60 / speed.to(ureg.mile_per_hour).magnitude
    else:
        continue

    if not debug:
      # Add to the database
      if initial:
        try:
          cur_country = db.session.query(Country).filter(Country.name==location['address']['country_code']).one()
        except:
          cur_country = Country(name=location['address']['country_code'])
        try:
          cur_state = db.session.query(State).filter(State.name==location['address']['state']).one()
        except:
          cur_state = State(name=location['address']['state'], country=cur_country)
        try:
          cur_city = db.session.query(City).filter(City.name==location['address']['city']).one()
        except:
          cur_city = City(name=location['address']['city'], state=cur_state)

        cur_run = Run(cur_city)
        cur_leg = Leg(cur_run)
        db.session.add_all([cur_country, cur_state, cur_city, cur_run, cur_leg])

        initial = False
      point = Point(local_time, elevation.magnitude, lat, lng, distance.to(ureg.meter).magnitude, speed.magnitude, cur_leg, cur_run)
      db.session.add(point)

    output_str = []
    output_str.append(f" * datetime: {local_time.strftime('%Y-%m-%D %H:%M:%S')}")
    output_str.append(f" * timezone: {timezone}")
    output_str.append(f" * location: {lat},{lng}")
    if 'city' in location['address']:
      output_str.append(f" * city: {location['address']['city']}")
    else:
      output_str.append(f" * city: {None}")
    if 'state' in location['address']:
      output_str.append(f" * state: {location['address']['state']}")
    else:
      output_str.append(f" * state: {None}")
    if 'country_code' in location['address']:
      output_str.append(f" * country: {location['address']['country_code']}")
    else:
      output_str.append(f" * country: {None}")
    output_str.append(f" * distance: {distance.to(ureg.mile):02.2~}")
    output_str.append(f" * elevation: {elevation.to(ureg.foot):.5~}")
    output_str.append(f" * speed: {speed.to(ureg.mile / ureg.hour):.3~}")
    output_str.append(f" * pace: {round(pace):02}:{round((pace % 1) * 60):02} min / mi")

    print(f"record: {local_time.strftime('%Y-%m-%D %H:%M:%S')}")
    print('\n'.join(output_str))
    print()
  if not debug:
    db.session.commit()

if __name__ == '__main__':
    parse_run()