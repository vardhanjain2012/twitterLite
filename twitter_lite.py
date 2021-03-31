import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import signal
import sys

def signal_handler(sig, frame):
	con.close()
	print('You pressed Ctrl+C!')
	sys.exit(0)


# for Vardhan
con = psycopg2.connect(dbname='flights_airports', user='postgres', host='localhost', password='MANGO')

# for Ashish
# con = psycopg2.connect(dbname='assignment2', user='postgres', host='localhost', password='490023')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("entry.html", message="Hello Flask!")

@app.route('/feed/<username>')
def feed(username):
	cur = con.cursor()
	cur.execute("SELECT * FROM flights WHERE carrier=%s", [username])
	items = cur.fetchall()
	cur.close()
	return render_template("feed.html", message="Hello Flask!", flights=items)

@app.route('/handle_data', methods=['POST'])
def handle_data_signup():
	username = request.form['email']
	psw = request.form['psw']
	pswrepeat = request.form['psw-repeat']
	return redirect(url_for('feed', username=username))

@app.route('/handle_data', methods=['POST'])
def handle_data_login():
	username = request.form['email']
	psw = request.form['psw']
	return redirect(url_for('feed', username=username))




if __name__ == "__main__":
	signal(SIGINT, handler)
	app.run(debug=True)