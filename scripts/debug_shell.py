import os
import sys

##########################################
# setup configuration and path for imports
###########################################
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

##########################################
# Import the application components
##########################################
from run import run_app
from run import db
from run.models import Country, State, City, Run, Leg, Point
from run import ureg, Q_

##########################################
# Create a sample
##########################################

##########################################
## Start the ipython shell
##########################################
from IPython import embed
embed()
