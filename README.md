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

A diagrammatic figure is also included for assistance below.
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

The relevant configuration files are provided in `etc/*` of this repo. 

#### Firewall Rules
One additional step is to adjust the systems firewall rules to enable connected clients to the WIFI Pineapple to access the internet through IP masquerading. This can be achieved with the command below.
```
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
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

### Developed Software 

#### The Configurator
A pen-tester must be able to monitor the system when it is live. Consequently, a configurator app was put together to help streamline some of the key configuration tasks and allow easy access to some information streams that could be of use to an attacker. The configurator app has four main screens; Clients, Routing, Traffic and Config. The application was built on flask and is located in `configurator/*` of this repo. The configurator is hosted at `192.168.5.1` locally by the Raspberry Pi. 

#### Example Website[1234] 
An indicative phishing website a pen-tester/attacker might host on one of the four IP's `192.168.4.[1234]` is provided in `phishing_site/*` of this repo. It is a basic website designed for credential harvesting and only provided as a proof of concept for the WIFI pineapple itself.

### Experimentation 
#### SSID Spoofing

SSID Spoofing was tested with the following method accross a variety of devices. 

##### Method 
1.	Connect target device to a genuine open wireless network. 
2.	Disconnect target device.
3.	Configure WIFI Pineapple to imitate the SSID of the genuine network. 
4.	Broadcast WIFI Pineapple AP.
5.	Bring device within vicinity of WIFI Pineapple AP.
6.	Observe results.
7.	Repeat for all devices. 
8.	Repeat for a closed wireless network.

##### Results
|     Device                  |     Result   and Observations (open AP)    |     Results   and Observations (closed AP)    |
|-----------------------------|--------------------------------------------|-----------------------------------------------|
|     Apple Macbook Pro M1    |     spoofed                                |     spoofed                                   |
|     Apple iPhone 11         |     spoofed                                |     spoofed                                   |
|     Dell Latitude 5530      |     spoofed                                |     spoofed                                   |

#### DNS Spoofing
The experiment tested the effectiveness of DNS spoofing across several websites. The target websites were categorised as, http only websites and http websites upgradeable to https (301 redirect) and those employing HSTS (http strict transport security). The browser used to conduct this experiment was Brave. Brave also has inbuilt a preloaded set of HSTS headers for high-profile websites. The websites, their classes and their descriptions are given in the table below:


|     Website                    |     Description                                                   |     Category                       |
|--------------------------------|-------------------------------------------------------------------|------------------------------------|
|     eu.httpbin.org             |     Service to demonstrate HTTP Requests and Responses            |     HTTP only                      |
|     sneaindia.com/index.php    |     A community board for an association, located in India.       |     HTTP only                      |
|     www.washington.edu         |     A university website                                          |     HTTP  - 301 Redirect           |
|     www.myshopify.com          |     The landing page for shopify, a popular ecomm application.    |     HTTP - 301 Redirect            |
|     www.baidu.com              |     A search engine prominently used in China.                    |     HSTS                           |
|     www.btcmarkets.net         |     A cryptocurrency trading platform                             |     HSTS                           |
|     www.google.com             |     A prominent global search engine                              |     HSTS – preloaded in browser    |
|     www.facebook.com           |     A prominent global social media website                       |     HSTS – preloaded in browser    |

#### Method 
1.	Configure WIFI Pineapple to route requests to website to malicious website 
2.	Clear browser DNS cache.
3.	Connect device to WIFI Pineapple AP 
4.	Navigate to website URL 
5.	Observe results 
6.	Repeat for each website 

##### Results
|     Website                    |     Result        |
|--------------------------------|-------------------|
|     eu.httpbin.org             |     pwnd!         |
|     sneaindia.com/index.php    |     pwnd!         |
|     www.washington.edu         |     pwnd!         |
|     www.myshopify.com          |     pwnd!         |
|     www.baidu.com              |     pwnd!         |
|     www.btcmarkets.net         |     pwnd!         |
|     www.google.com             |     safe          |
|     www.facebook.com           |     safe          |