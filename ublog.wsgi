"""WSGI script for uwsgi"""

import os
import site

os.environ['PYTHON_EGG_CACHE'] = '../python_egg'

# Import the project and create a WSGI application object
import blog

application = blog.main()
