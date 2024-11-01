import sqlite3

connection = sqlite3.connect('resources/database.db')


with open('schema.sql') as f:
	connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO domains (domain_url, domain_ip) VALUES (?, ?)",
			('', '192.168.4.1')
			)

cur.execute("INSERT INTO domains (domain_url, domain_ip) VALUES (?, ?)",
			('', '192.168.4.2')
			)

cur.execute("INSERT INTO domains (domain_url, domain_ip) VALUES (?, ?)",
			('', '192.168.4.3')
			)

cur.execute("INSERT INTO domains (domain_url, domain_ip) VALUES (?, ?)",
			('', '192.168.4.4')
			)

cur.execute("INSERT INTO domains (domain_url, domain_ip) VALUES (?, ?)",
			('', '192.168.4.5')
			)

cur.execute("""
			INSERT INTO configs (config_id, config_value, config_description) 
			VALUES 
			('configs.parent_ssid', 'TP-Link', 'SSID of the network this device connects too'),
			('configs.parent_hasPassword', 'TRUE', ''),
			('configs.parent_password', 'password', 'Password of the network this device connects too'),
			('configs.device_ssid', 'TP-Link-LOL', 'SSID of the network this device broadcasts. Typically the same as the parent ssid for pineapples'),
			('configs.device_hasPassword', 'TRUE', ''),
			('configs.device_password', 'password', 'Password of the network this device broadcasts');
			""")

connection.commit()
connection.close()
