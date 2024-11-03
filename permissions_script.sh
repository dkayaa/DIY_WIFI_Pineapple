echo "replace directories" 
sudo rm -r /var/www/configurator
sudo rm -r /var/www/phishing_site

cp -r /repos/COMP6841_SAP/configurator /var/www/configurator
cp -r /repos/COMP6841_SAP/phishing_site /var/www/phishing_site

echo "replace directories - done"

echo "Setting Permissions" 

sudo chown www-data:www-data /etc/hostapd
sudo chown www-data:www-data /etc/hostapd/hostapd.conf 
sudo chown www-data:www-data /etc/dnsmasq.conf
sudo chown www-data:www-data /var/www/configurator
sudo chown www-data:www-data /var/www/configurator/resources
sudo chown www-data:www-data /var/www/configurator/resources/database.db
sudo chown www-data:www-data /var/www/configurator/resources/traffic
sudo chown www-data:www-data /var/www/configurator/sniffer.py


sudo chown www-data:www-data /var/www/phishing_site/resources/credentials.txt
sudo chown www-data:www-data /var/www/phishing_site/resources
sudo chown www-data:www-data /var/www/phishing_site

sudo chmod 777 /etc
sudo chmod 777 /etc/dnsmasq.conf
sudo chmod 777 /etc/hostapd
sudo chmod 777 /etc/hostapd/hostapd.conf

sudo chmod 777 /var/www/configurator
sudo chmod 777 /var/www/configurator/resources
sudo chmod 777 /var/www/configurator/resources/database.db
sudo chmod 777 /var/www/configurator/resources/traffic
sudo chmod 777 /var/www/configurator/sniffer.py 
sudo chmod 777 /var/www/configurator/my_configs.py
sudo chmod 777 /var/www/phishing_site/resources/credentials.txt
sudo chmod 777 /var/www/phishing_site/my_configs.py
echo "Setting Permissions - Done"

echo "restarting apache2"
sudo systemctl reload apache2
sudo systemctl restart apache2
echo "restarting apache2 - Done"
