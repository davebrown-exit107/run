import os
import sys

##########################################
# setup configuration and path for imports
###########################################
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

from run import db
from run import run_app
from run.models import Country, State, City, Run, Leg, Point

def clear_db(db):
  confirm = input('Clear all tables? [yes/no]: ')
  if confirm == 'yes':
    # drop/create tables
    print('#'*60)
    print('Dropping all tables')
    print('#'*60)
    db.drop_all()
    print('#'*60)
    print('Creating all tables')
    print('#'*60)
    db.create_all()
    print('All tables cleared')
  elif confirm == 'no':
    exit(1)
  else:
    print('Please type yes or no')
    clear_db(db)

if __name__ == '__main__':
  clear_db(db)
