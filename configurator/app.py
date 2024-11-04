import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import os
import subprocess
import csv
import subprocess

from my_configs import add_my_configs

add_my_configs()
dnsmasq_path = os.environ['dnsmasq_path']
hostapd_path = os.environ['hostapd_path']
db_connection_string = os.environ['db_connection_string']


traffic_csv = os.environ['traffic_csv_path']


command = ['sudo', os.environ["python3_path"], os.environ["sniffer_path"]]
subprocess.Popen(command) 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["configurator_secret_key"]

os.system(f"sudo chmod 644 {dnsmasq_path}")

def get_db_connection():
	conn = sqlite3.connect(db_connection_string)
	conn.row_factory = sqlite3.Row
	return conn

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/routing_page', methods=('GET', 'POST')) 
def routing_page():

	conn = get_db_connection()
	domains = conn.execute('SELECT * FROM domains').fetchall()
	domain_ips = conn.execute('SELECT domain_ip FROM domains').fetchall()

	conn.close()

	if request.method == 'POST':

		domain_url = request.form['domain_url'].strip()
		domain_ip = request.form['domain_ip'].strip()
		
		if not domain_ip:
			flash('Domain IP is required!')
		else:
			conn = get_db_connection()
			conn.execute(
				""" UPDATE domains  
				SET domain_url = ?, 
				modified = CURRENT_TIMESTAMP 
				WHERE  
				domain_ip = ? """, (domain_url, domain_ip))
			conn.commit()
			conn.close()
			
			#update dnsmasq config 
			with open(dnsmasq_path, 'w') as file:
				file.write("""interface=wlan0
#define 18 address leases for a duration of 24 hours 
dhcp-range=192.168.29.2,192.168.29.30,255.255.255.0,24h
#domain=wlan
#prevent dnsmasq from using resolv.conf(which configures the systems DNS resolver)
#no-resolv
local-ttl=3600
#DNS Mappings
#configurator
address=/mypineapple.config.local/192.168.5.1"""	
				)
				conn = get_db_connection()
				domains2 = conn.execute('SELECT * FROM domains').fetchall()
				for domain in domains2:
					if domain['domain_url'] and domain['domain_url']:
						file.write(f"""
#Website {domain['domain_url']}
address=/{domain['domain_url']}/{domain['domain_ip']}
#no upstream dns server for this url
server=/{domain['domain_url']}/0.0.0.0"""
					)
				conn.close()	
			
			#restart dnsmasq
			os.system(f"sudo systemctl restart dnsmasq")
			return redirect(url_for('routing_page'))
	return render_template('routing_page.html', domains=domains, domain_ips=domain_ips)
		
@app.route('/clients_page')
def clients_page():
    #execute the below , parse and store in client table.
    #iw dev wlan0 station dump | grep ^.*Station.*$
    conn = get_db_connection()
    try:
        result = subprocess.run(['iw', 'dev', 'wlan0', 'station', 'dump'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.split('\n')
        mac_addresses = [line.split()[1] for line in lines if line.startswith('Station')]
        conn.execute('DELETE FROM clients')
        print(mac_addresses)
        for mac in mac_addresses:
            conn.execute("INSERT OR IGNORE INTO clients (client_id, is_connected) VALUES (?, ?)", (mac, 'TRUE'))
        conn.commit()
    except Exception as e:
        print(f"Exception Raised: {e}")
    clients = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('clients_page.html', clients=clients)

@app.route('/traffic_page', methods=('GET', 'POST'))
def traffic_page():

    records = []

    with open(traffic_csv, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            records.append(row)

    return render_template('traffic_page.html', records=records)

@app.route('/configs_page', methods=('GET', 'POST'))
def configs_page():
    if request.method == 'POST':
        if "update_table" in request.form:
            config_value = request.form['config_value'].strip()
            config_id = request.form['config_id'].strip()

            if not config_id:
                flash('Config ID is required!')
            else:
                conn = get_db_connection()
                conn.execute(
                    """ UPDATE configs  
                    SET config_value = ?, 
                    modified = CURRENT_TIMESTAMP 
                    WHERE  
                    config_id = ? """, (config_value, config_id))
                conn.commit()
                conn.close()
        if "update_configs" in request.form:
                #update hostapd
                conn = get_db_connection()
                with open(hostapd_path, 'w') as file:
                    config_device_ssid = conn.execute("SELECT * FROM configs WHERE config_id = \"configs.device_ssid\"").fetchall()[0]
                    config_device_hasPassword = conn.execute("SELECT * FROM configs WHERE config_id = \"configs.device_hasPassword\"").fetchall()[0]
                    config_device_password = conn.execute("SELECT * FROM configs WHERE config_id = \"configs.device_password\"").fetchall()[0]
                    if config_device_ssid['config_value']:
                        file.write(f"""
# the interface used by the AP
interface=wlan0
driver=nl80211
# "g" simply means 2.4GHz band
hw_mode=g
# the channel to use
channel=1
# limit the frequencies used to those allowed in the country
ieee80211d=1
# the country code
country_code=AU
# 802.11n support
ieee80211n=1
# QoS support, also required for full speed on 802.11n/ac/ax
wmm_enabled=1
# the name of the AP
ssid={config_device_ssid['config_value'].strip()}
# 1=wpa, 2=wep, 3=both
auth_algs=1
ignore_broadcast_ssid=0""")
                        
                    if config_device_hasPassword['config_value'] == 'TRUE': 
                        file.write(f"""
# WPA2 only
wpa=2
wpa_passphrase={config_device_password['config_value'].strip()}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP""")
                #restart hostapd 
                os.system(f"sudo systemctl restart hostapd")
                config_parent_ssid = conn.execute("SELECT * FROM configs WHERE config_id = \"configs.parent_ssid\"").fetchall()[0]
                config_parent_hasPassword = conn.execute("SELECT * FROM configs WHERE config_id = \"configs.parent_hasPassword\"").fetchall()[0]
                config_parent_password = conn.execute("SELECT * FROM configs WHERE config_id = \"configs.parent_password\"").fetchall()[0]			
                if (config_parent_ssid['config_value']):
                    if (config_parent_hasPassword['config_value']) == 'TRUE' and config_parent_password['config_value']:
                        #protected SSID
                        os.system(f"nmcli device wifi connect \"{config_parent_ssid['config_value']}\" password \"{config_parent_password['config_value']}\"")
                        print(f"nmcli device wifi connect \"{config_parent_ssid['config_value'].strip()}\" password \"{config_parent_password['config_value'].strip()}\"")
                    else:
                        #open SSID
                        os.system(f"nmcli device wifi connect \"{config_parent_ssid['config_value']}\"")
                        print(f"nmcli device wifi connect \"{config_parent_ssid['config_value'].strip()}\"")
                conn.close()	
                return redirect(url_for('configs_page'))

    conn = get_db_connection()
    configs = conn.execute('SELECT * FROM configs').fetchall()
    config_ids = conn.execute('SELECT config_id FROM configs').fetchall()

    conn.close()
    return render_template('configs_page.html', configs=configs, config_ids=config_ids)
