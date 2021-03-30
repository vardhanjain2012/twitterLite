import psycopg2, psycopg2.extras
from flask import Flask, render_template

app = Flask(__name__, static_folder='../static')

@app.route('/')
def hello_world():
    return render_template("entry.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/feed')
def feed():
    return render_template("feed.html", message="Hello Flask!")

#TODO: make it posonalized for user and use tweet times
@app.route('/explore')
def explore():
    con = psycopg2.connect(dbname='twitter_lite', user='postgres', host='localhost', password='490023')
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    pop_users_by_replies_q ='''SELECT u.name, count(*) as n_replies
                            FROM tweets_withoutwords as t, user_map as u
                            WHERE u.name = t.reply_to_user
                            GROUP BY u.name
                            ORDER BY n_replies desc
                            LIMIT 10'''

    cur.execute(pop_users_by_replies_q)

    pop_users_by_replies = cur.fetchall()

    con.commit()
    cur.close()
    con.close()
    return render_template("explore.html", pop_users_by_replies = pop_users_by_replies)

# @app.route('/profile/')
# def explore():
#     con = psycopg2.connect(dbname='twitter_lite', user='postgres', host='localhost', password='490023')
#     cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
#     pop_users_by_replies_q ='''SELECT u.name, count(*) as n_replies
#                             FROM tweets_withoutwords as t, user_map as u
#                             WHERE u.name = t.reply_to_user
#                             GROUP BY u.name
#                             ORDER BY n_replies desc
#                             LIMIT 10'''

#     cur.execute(pop_users_by_replies_q)

#     pop_users_by_replies = cur.fetchall()

#     con.commit()
#     cur.close()
#     con.close()
#     return render_template("explore.html", pop_users_by_replies = pop_users_by_replies)


if __name__ == "__main__":
    
    app.run(debug=True)
    