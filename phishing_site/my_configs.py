import os

def add_my_configs():
    if "dep_path" not in os.environ:
        os.environ["dep_path"] = '/home/deniz_kaya/pvenv/myenv/lib/python3.11/site-packages'

    if "configurator_path" not in os.environ:
        os.environ["configurator_path"] = '/var/www/configurator'

    if "phishing_site_path" not in os.environ:
        os.environ["phishing_site_path"] = '/var/www/phishing_site'

    if "traffic_csv_path" not in os.environ:
        os.environ["traffic_csv_path"] = './resources/traffic'

    #if "traffic_csv_path" not in os.environ:
    #    os.environ["traffic_csv_path"] = '/var/www/configurator/resources/traffic'

    if "dnsmasq_path" not in os.environ:
        os.environ["dnsmasq_path"] = './tests/dnsmasq2.conf'

    #if "dnsmasq_path" not in os.environ:
    #    os.environ["dnsmasq_path"] = '/etc/dnsmasq.conf'

    if "hostapd_path" not in os.environ:
        os.environ["hostapd_path"] = './tests/hostapd2.conf'

    #if "hostapd_path" not in os.environ:
    #    os.environ["hostapd_path"] = '/etc/hostapd/hostapd.conf'

    if "db_connection_string" not in os.environ:
        os.environ["db_connection_string"] = './resources/database.db'

    #if "db_connection_string" not in os.environ:
    #    os.environ["db_connection_string"] = '/var/www/configurator/resources/database.db'

    if "python3_path" not in os.environ: 
        os.environ["python3_path"] = 'python3'

    #if "python3_path" not in os.environ: 
    #    os.environ["python3_path"] = '/home/deniz_kaya/pvenv/myenv/bin/python3.11'

    if "sniffer_path" not in os.environ: 
        os.environ["sniffer_path"] = "./sniffer.py"

    #if "sniffer_path" not in os.environ: 
    #    os.environ["sniffer_path"] = "/var/www/configurator/sniffer.py"

    if "sniffer_target_interface" not in os.environ:
        os.environ["sniffer_target_interface"] = 'en0'

    #if "sniffer_target_interface" not in os.environ:
    #    os.environ["sniffer_target_interface"] = 'wlan1'

    if "configurator_secret_key" not in os.environ:
        os.environ["configurator_secret_key"] = 'pineapple@2024'

    if "phishing_site_credentials_path" not in os.environ:
        os.environ["phishing_site_credentials_path"] = './resources/credentials.txt'

    #if "phishing_site_credentials_path" not in os.environ:
    #    os.environ["phishing_site_credentials_path"] = '/var/www/phishing_site/resources/credentials.txt'