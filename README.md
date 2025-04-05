# DIY WIFI Pineapple 

A WIFI pineapple is a network security tool that cyber security experts, pen-testers and malicious attackers use. It is a tool that is commonly used to detect company network vulnerabilities. What makes it so powerful is that it enables the controller to record, analyse and modify the internet traffic which travels through it. Naturally, this makes it a very popular tool amongst cyber security criminals, as it enables them exploit client devices through attacks such as man in the middle attacks, SSID Spoofing and DNS Spoofing. The goal of this repo is to explore the capabilities of a WIFI Pineapple through development using free open-source software. The intention of this repo is not to motivate malicious attackers, but rather to bring into the limelight the ever-present danger of WIFI pineapples and the seemingly invisible yet significant risks when doing something as innocent as accessing an open public Wi-Fi network.

## The Build 
### Hardware

| Item                              | Quantity |
|-----------------------------------|----------|
| Raspberry Pi 3 Model B+           | 1        |
| Ethernet Cable                    | 1        |
| TP-Link Wireless USB WIFI Adapter | 1        |

### OS
Theoperatingsystemusedwas: `Debian GNU/Linux 12`
The operating system was installed on the Raspberry Pi using the raspberry pi imaging software.

### Network Interfaces 
Off the shelf, the raspberry pi ofers two network interfaces, an ethernet and a wireless interface (denotes as eth0 and wlan1). This is insufficient for a WIFI pineapple as it requires two wireless interfaces. A secondary wireless interface is introduced by purchasing an off the shelf USB WIFI adapter. The interfaces and their uses are outlined in the table below.

| Interface | Description                                      | Notes                                                                                                                         |
|-----------|--------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| eth0      | Ethernet interface (built-in)                    | Unused in the context of an attack, or only used to locally ssh into the machine to access files/ make configuration changes. |
| wlan0     | Wireless interface from the wireless USB adaptor | Connects to client devices (victim devices)                                                                                   |
| wlan1     | Wireless interface (built-in)                    | Connects to upstream modem/ router (the genuine access point)                                                                 |
 ![Network Interfaces](/img/interfaces.png)

 ### Third Party Modules 

```
root@raspberrypi:/# sudo apt-get update
root@raspberrypi:/# sudo apt-get install dnsmasq
root@raspberrypi:/# sudo apt-get install hostapd
root@raspberrypi:/# sudo apt-get install dhcpcd
root@raspberrypi:/# sudo apt-get install apache2

root@raspberrypi:/# python3 -m venv /venv
root@raspberrypi:/# source /venv/bin/activate
(venv) root@raspberrypi:/# python3 -m pip install flask
(venv) root@raspberrypi:/# python3 -m pip install scapy
```

#### Apache2 
In the context of this project, there is particular interest in this module as it will be used to host the phishing websites attackers/pen-testers might use during DNS Spoofing. This is possible through apache2’s virtual host functionality. That is, apache2 can host multiple websites on the same device, using what are called virtual hosts. For this project, 5 virtual hosts have been set up with the following roles and IP’s:

| Virtual Host ID | IP          | Description            |
|-----------------|-------------|------------------------|
| 1               | 192.168.5.1 | Hosts Configuration UI |
| 2               | 192.168.4.1 | Hosts Website 1        |
| 3               | 192.168.4.2 | Hosts Website 2        |
| 4               | 192.168.4.3 | Hosts Website 3        |
| 5               | 192.168.4.4 | Hosts Website 4        |

the related configurations can be viewed in `etc/apache2/*`
