
# Load the config file, and create variables
# that can be referenced within other files

import json
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open( BASE_DIR + "/config/config.json", "r" ) as configFile :
	data = configFile.read( )

data = json.loads( data )

# DATABASE VARS
DB_HOST = data['DB']['DB_HOST']
DB_USER = data['DB']['DB_USER']
DB_PASS = data['DB']['DB_PASS']
DB_NAME = data['DB']['DB_NAME']
DB_QUICK = data['DB']['DB_QUICK']