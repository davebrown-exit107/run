# pylint: disable=wrong-import-position
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring

import os
import sys

from werkzeug.middleware.shared_data import SharedDataMiddleware

##########################################
# setup configuration and path for imports
###########################################
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(root_dir)

from run import run_app

# serve the static files from flask for dev work
run_app.wsgi_app = SharedDataMiddleware(run_app.wsgi_app, {
    '/': os.path.join(os.path.dirname(__file__), '/static')
})

run_app.debug = True
run_app.run(host='0.0.0.0', port=5050)
