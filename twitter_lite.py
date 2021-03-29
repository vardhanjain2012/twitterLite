import psycopg2
from flask import Flask, render_template

# for Vardhan
# con = psycopg2.connect(dbname='flights_airports', user='postgres', host='localhost', password='MANGO')

# for Ashish
con = psycopg2.connect(dbname='assignment2', user='postgres', host='localhost', password='490023')

cur = con.cursor()

cur.execute("SELECT * FROM flights")
items = cur.fetchall()


cur.close()
con.close()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("entry.html", message="Hello Flask!", flights = items)

@app.route('/login')
def login():
    return render_template("login.html", message="Hello Flask!", flights = items)

@app.route('/signup')
def signup():
    return render_template("signup.html", message="Hello Flask!", flights = items)

@app.route('/feed')
def feed():
    return render_template("feed.html", message="Hello Flask!", flights = items)


if __name__ == "__main__":
    app.run(debug=True)