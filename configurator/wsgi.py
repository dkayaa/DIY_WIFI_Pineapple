
import sys
dep_path =  '/home/deniz_kaya/pvenv/myenv/lib/python3.11/site-packages'
sys.path.insert(0, dep_path)
sys.path.insert(0, '/var/www/configurator')

from app import app as application 
