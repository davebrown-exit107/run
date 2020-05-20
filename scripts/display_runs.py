import os
from pprint import pprint
import sys
from time import sleep

import requests

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

from run import run_app
from run import db
#from run.models import Info, Group, Year, Bulletin, Vulnerability, Product, Vendor, CVE
#from run.lib import get_proxies, get_bulletin_years, get_bulletin_contents, get_bulletins, get_cve

#proxies = get_proxies(run_app.config)

#bulletin_uri = run_app.config.get('BULLETIN_BASE_URI')
