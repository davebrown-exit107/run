#from datetime import datetime, date, time
#import os
#import sys
#
###########################################
## 3rd party modules
############################################
#import ipdb
#from IPython import embed
#from geopy.geocoders import OpenMapQuest
#from timezonefinder import TimezoneFinder
#
###########################################
## setup configuration and path for imports
############################################
#root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#sys.path.append(root_dir)
#
###########################################
## Import the run components
###########################################
#from run import db
#from run.lib import *
#from run.models import Country, State, City, Run, Point, Leg
#
## Build our api instances
#geocoder = OpenMapQuest(api_key=OPEN_MAPQUEST_KEY, scheme='http')
#tf = TimezoneFinder()
#ureg = UnitRegistry()
#
#lat = convert_to_degrees(559289458)
#lng = convert_to_degrees(-1360110105)
#
#location = reverse_geocode(gmaps,lat,lng)
#cur_tz = Timezone(name=find_timezone(tf,lat,lng))
#
#us = Country(name=location['country'])
#
#mt = State(name=location['state'])
##mt = State(name='Montana', country=us)
#
#msla = City(name=location['city'])
##msla = City(name='Missoula', state=mt)
#
#mon = Day(sunrise=time(0,26,0), sunset=time(2,59,0), date=date(2016,8,8))
#
#run = Run(avg_speed=2.51,
#          max_speed=3.228,
#          start_position_lat=convert_to_degrees(559289458),
#          start_position_long=convert_to_degrees(-1360110105),
#          end_position_lat=convert_to_degrees(-1360110105),
#          end_position_long=convert_to_degrees(-1359922776),
#          total_ascent=234,
#          total_descent=234,
#          total_distance=5.02,
#          start_time=datetime(2016,8,8,12,5,5),
#          total_timer_time=550398,
#          state=mt,
#          total_elapsed_time=550398,
#          city=msla,
#          country=us,
#          timezone=cur_tz,
#          #timezone=mst,
#          day=mon,
#          )
#
##db.session.add_all([cur_tz, us, mt, msla, mon, run])
##db.session.commit()
#
#embed(header='post-record creation, pre-record submission')
##ipdb.set_trace()
#