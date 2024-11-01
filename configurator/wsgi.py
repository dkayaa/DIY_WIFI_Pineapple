
import sys
import os 
dep_path =  '/home/deniz_kaya/pvenv/myenv/lib/python3.11/site-packages'
sys.path.insert(0, dep_path)
#os.environ['XDG_CONFIG_HOME'] = '/var/www/.config'
#os.environ['XDG_CACHE_HOME'] = '/var/www/.cache'
#os.environ['SCAPY_CONFIG_FOLDER'] = '/var/www/.config/'
# Add the application directory to the sys.path
sys.path.insert(0, '/var/www/configurator')

from app import app as application 
