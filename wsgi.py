# PythonAnywhere WSGI configuration
# Point your Web app's WSGI config to this file

import sys
import os

# Add your project directory to the Python path
project_home = '/home/YOUR_USERNAME/rental-manager'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from app import application
