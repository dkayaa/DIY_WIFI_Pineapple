
from scapy.all import sniff
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.all import conf

import threading

traffic_csv = '/var/www/configurator/resources/traffic'
#traffic_csv = './resources/traffic'

# Define a callback function to process captured packets
def process_packet(packet):
    with open(traffic_csv, 'a') as f:
        if packet.haslayer(HTTPRequest):
            http_request = packet[HTTPRequest]
            f.write(f"HTTP Request\t{http_request.Method.decode()}\t {http_request.Host.decode()}\t {http_request.Path.decode()} \n")
            #print(f"HTTP Request\t {http_request.Method.decode()}\t {http_request.Host.decode()}\t {http_request.Path.decode()}")
        elif packet.haslayer(HTTPResponse):
            http_response = packet[HTTPResponse]
            f.write(f"HTTP Response\t {http_response.Status_Code.decode()}\t \t \n")
            #print(f"HTTP Response\t {http_response.Status_Code.decode()}\t \t")

def traffic_process():
    # Start sniffing on the desired interface (replace 'eth0' with your interface)
    #sniff(iface='en0', filter='tcp port 80', prn=process_packet, store=0) 
    sniff(iface='wlan0', filter='tcp port 80', prn=process_packet, store=0) 



thread = threading.Thread(target=traffic_process)
thread.start()

