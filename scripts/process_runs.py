import argparse
from datetime import datetime, date, time
import sys
import os
import sys

##########################################
# 3rd party modules
###########################################
import json
import pendulum
import requests

from fitparse import FitFile, FitParseError
from geopy.geocoders import OpenMapQuest
from path import Path
from pint import UnitRegistry
from timezonefinder import TimezoneFinder

##########################################
# setup configuration and path for imports
###########################################
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

##########################################
# import run libraries
###########################################
from run import run_app
from run import db
from run.lib import *
from run.models import Country, State, City, Run, Leg, Point

##########################################
# Open the file named on the command line
###########################################
#TODO: Move this to click
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file', type=argparse.FileType('r'), nargs=1,
                    help='File to be parsed (.fit)')

args = parser.parse_args()
input_file_path = Path(args.file[0].name)

##########################################
# Parse the fit file
###########################################
with open(input_file_path, 'rb') as input_file:
  try:
    fitfile = FitFile(input_file, check_crc=False)
    fitfile.parse()
  except FitParseError as err:
    print('Error while parsing {}: {}'.format(input_file.relpath(), err))
    sys.exit(1)

##########################################
# Build our api instance
##########################################
geocoder = OpenMapQuest(api_key=run_app.config['OPEN_MAPQUEST_KEY'], schema='http')
tf = TimezoneFinder()
ureg = UnitRegistry()

##########################################
# Start processing the file
##########################################
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
for i, record in enumerate(fit_file.messages):
  if record.mesg_num == 20:
    #############################################
    # Get the location data. We'll move to the next record if the location information is bad.
    #############################################
    lat = convert_to_degrees(record.get_value('position_lat'))
    lng = convert_to_degrees(record.get_value('position_long'))
    if lat and lng:
      timezone = find_timezone(tf,lat,lng)
    else:
      print('Bad Location Data')
      continue

    #############################################
    # Sometimes speed is set to 0
    #############################################
    if 0 == record.get_value('enhanced_speed'):
      continue

    #############################################
    # Get the time data
    #############################################
    # store in utc, we'll convert later. This is just easier and allows for more flexibility.
    print(record.get_value('timestamp'))
    print(type(record.get_value('timestamp')))
    utc_time = pendulum.instance(record.get_value('timestamp'))
    # local is for weather only
    local_tz = pendulum.timezone(timezone)
    local_time = local_tz.convert(utc_time)

    if (local_time.hour,local_time.minute) not in moments:
      moments.append((local_time.hour,local_time.minute))

      #############################################
      # Get the location data.
      #############################################
      location = geocoder.reverse([lat,lng]).raw

#      #############################################
#      # Get the weather/sunrise/sunset data
#      #############################################
#      uri = 'https://api.forecast.io/forecast/{api_key}/{lat},{lng},{time}'.format(
#            api_key=FORECAST_API_KEY,
#            time=local_time.isoformat(),
#            lat=lat,
#            lng=lng)
#
#      resp = requests.get(uri)
#      weather = json.loads(resp.text)

      #############################################
      # First record to establish some daily data
      #############################################
#      if initial:
#        # These are all UTC.
#        sunrise = pendulum.from_timestamp(weather['daily']['data'][0]['sunriseTime'])
#        sunset = pendulum.from_timestamp(weather['daily']['data'][0]['sunsetTime'])
#
#        day = Day(sunrise=sunrise, sunset=sunset, date=utc_time.date())
#
#        country = Country(name=location['country'])
#        state = State(name=location['state'])
#        #mt = State(name='Montana', country=us)
#        city = City(name=location['city'])
#        #msla = City(name='Missoula', state=mt)
#
#        import ipdb
#        ipdb.set_trace()
#
#        initial = False

# Now we begin processing in earnst
# First find the first record, this is our start time
# Now record all points, those will be linked to the run...?
# Watch for stop times initiated by lap events, those are obviously mile laps that will be linked to the run
# Watch for stop times initiated by "manual" events. That's either a full stop time or a watch stop time
# Final stop time "manual" is the end of our run.

#    try:
#      run = Run(avg_speed=2.51,
#                max_speed=3.228,
#                start_position_lat=convert_to_degrees(559289458),
#                start_position_long=convert_to_degrees(-1360110105),
#                end_position_lat=convert_to_degrees(-1360110105),
#                end_position_long=convert_to_degrees(-1359922776),
#                total_ascent=234,
#                total_descent=234,
#                total_distance=5.02,
#                start_time=datetime(2016,8,8,12,5,5),
#                total_timer_time=550398,
#                state=location['state'],
#                total_elapsed_time=550398,
#                city=location['city'],
#                country=location{'country'],
#                timezone=cur_tz,
#                #timezone=mst,
#                day=mon,
#                )
#      db.session.add(run)
#      db.session.flush()
#    except IntegrityError:
#      db.session.rollback()
#      cur_year=Run.query.filter_by(start_time=year).first()
#    db.session.commit()
#
#
#
#
#  run = Run(avg_speed=2.51,
#            max_speed=3.228,
#            start_position_lat=convert_to_degrees(559289458),
#            start_position_long=convert_to_degrees(-1360110105),
#            end_position_lat=convert_to_degrees(-1360110105),
#            end_position_long=convert_to_degrees(-1359922776),
#            total_ascent=234,
#            total_descent=234,
#            total_distance=5.02,
#            start_time=datetime(2016,8,8,12,5,5),
#            total_timer_time=550398,
#            state=mt,
#            total_elapsed_time=550398,
#            city=msla,
#            country=us,
#            timezone=cur_tz,
#            #timezone=mst,
#            day=mon,
#            )
#
#  #db.session.add_all([cur_tz, us, mt, msla, mon, run])
#  #db.session.commit()
#
#  embed(header='post-record creation, pre-record submission')
#  #ipdb.set_trace()
#
#              datetime=local_time.strftime('%Y-%m-%D %H:%M:%S'),
#              #datetime=local_time.to_day_datetime_string(),
#              timezone=timezone,
#              temp=weather.get('currently')['temperature'],
#              #temp=50,
#              lat=lat,
#              lng=lng,
#              city=location['city'],
#              state=location['state'],
#              country=location['country'],
#              dist=dist(record.get_value('distance')),
#              elevation=elevation(record.get_value('altitude')),
#              speed=speed(record.get_value('speed')),
#              split=split(record.get_value('speed'))
#              )
#        )
#        print('#'*50,'\n')
#  for year in years:
#    try:
#      cur_year=Year(year=year)
#      db.session.add(cur_year)
#      db.session.flush()
#    except IntegrityError:
#      db.session.rollback()
#      cur_year=Year.query.filter_by(year=year).first()
#    db.session.commit()
