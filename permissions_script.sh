echo "replace directories" 
sudo rm -r /var/www/configurator
sudo rm -r /var/www/phishing_site

cp -r /repos/COMP6841_SAP/configurator /var/www/configurator
cp -r /repos/COMP6841_SAP/phishing_site /var/www/phishing_site

echo "replace directories - done"

echo "Setting Permissions" 

sudo chown root:www-data /etc/dnsmasq.conf
sudo chown www-data:www-data /var/www/configurator/resources/database.db

sudo chmod 664 /etc
sudo chmod 664 /etc/dnsmasq.conf
sudo chmod 664 /etc/hostapd
sudo chmod 664 /etc/hostapd/hostapd.conf

sudo chmod 777 /var/www/configurator
sudo chmod 777 /var/www/configurator/resources
sudo chmod 777 /var/www/configurator/resources/database.db

echo "Setting Permissions - Done"

echo "restarting apache2"

sudo systemctl restart apache2
echo "restarting apache2 - Done"
