import sys
import os
import sys

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
from pint import UnitRegistry
from timezonefinder import TimezoneFinder

##########################################
# setup configuration and path for imports
###########################################
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

##########################################
# import application components
###########################################
from run import run_app
from run import db
from run.lib import *

##########################################
# Open the file named on the command line
###########################################
@click.command()
@click.argument("input", type=click.File("rb"), nargs=-1)
def debug_parse_run(input_file):

  ##########################################
  # Parse the fit file
  ###########################################
  try:
    fitfile_processor = StandardUnitsDataProcessor()
    fitfile = FitFile(input_file, data_processor=fitfile_processor, check_crc=False)
    fitfile.parse()
  except FitParseError as err:
    print('Error while parsing {}: {}'.format(input_file.relpath(), err))
    sys.exit(1)

  # Build our api instances
  geocoder = OpenMapQuest(api_key=run_app.config['OPEN_MAPQUEST_KEY'], scheme='http')
  tf = TimezoneFinder()
  ureg = UnitRegistry()

  # Pull manufacturer data
  for record in fitfile.get_messages('file_id', with_definitions=False): 
    manufacturer = record.get_value('manufacturer')
    product = record.get_value('garmin_product')

  for record in fitfile.get_messages('file_creator', with_definitions=False): 
    pass

  print(f"device: {manufacturer} -- {product}")

  # Parse all events
  for record in fitfile.get_messages('event', with_definitions=False): 
    event_group = record.get_value('event_group')
    timestamp = record.get_value('timestamp')
    print(f"event: {event_group} -- {timestamp}")
    for record_data in record: 
        print(f" * {record_data.name}: {record_data.value}")

  # Parse all records
  for record in fitfile.get_messages('record', with_definitions=False): 
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
    pace = 60 / speed.to(ureg.mile_per_hour).magnitude

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

if __name__ == '__main__':
    debug_parse_run()
