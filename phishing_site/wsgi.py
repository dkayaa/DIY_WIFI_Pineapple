
import sys
import os
sys.path.insert(0, '/var/www/phishing_site')
from my_configs import add_my_configs 
add_my_configs() 
dep_path =  os.environ["dep_path"]
sys.path.insert(0, dep_path)
from app import app as application 
