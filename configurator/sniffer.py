
from scapy.all import sniff
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.all import conf

import threading
from datetime import datetime

traffic_csv = '/var/www/configurator/resources/traffic'
#traffic_csv = './resources/traffic'

def process_packet(packet):
    with open(traffic_csv, 'a') as f:       
        if packet is not None:
            f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + f"\t" + \
                    packet.sniffed_on + f"\t" + \
                    packet.summary() + f"\n")


def traffic_process():
    #sniff(iface='en0', filter='tcp port 80', prn=process_packet, store=0) 
    sniff(iface='wlan1', filter='tcp port 80 or tcp port 443', prn=process_packet, store=0) 



thread = threading.Thread(target=traffic_process)
thread.start()

