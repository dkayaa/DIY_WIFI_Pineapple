
from scapy.all import sniff
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.all import conf

import threading
from datetime import datetime

traffic_csv = '/var/www/configurator/resources/traffic'
#traffic_csv = './resources/traffic'

# Define a callback function to process captured packets
def process_packet(packet):
    with open(traffic_csv, 'a') as f:       
        if packet is not None:
            f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + f"\t" + \
                    packet.sniffed_on + f"\t" + \
                    packet.summary() + f"\n")


def traffic_process():
    # Start sniffing on the desired interface (replace 'eth0' with your interface)
    #sniff(iface='en0', filter='tcp port 80', prn=process_packet, store=0) 
    sniff(iface='wlan0', filter='tcp port 80', prn=process_packet, store=0) 



thread = threading.Thread(target=traffic_process)
thread.start()

