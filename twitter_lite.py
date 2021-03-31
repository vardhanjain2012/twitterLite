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
                            LIMIT 100'''
    
    cur.execute(pop_users_by_replies_q)

    pop_users_by_replies = cur.fetchall()

    con.commit()
    cur.close()

    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    trending_hashtags_q = '''SELECT links[s] AS tag, count(*) AS count
                        FROM
                        (SELECT id,generate_subscripts(link_types, 1) AS s, link_types, links
                            FROM tweets_withoutwords_staging) AS foo
                        WHERE link_types[s] = 'hashtag'
                        GROUP BY links[s]
                        ORDER BY count desc
                        LIMIT 100'''

    cur.execute(trending_hashtags_q)

    trending_hashtags = cur.fetchall()

    con.commit()
    cur.close()

    con.close()
  
    return render_template("explore.html", pop_users_by_replies = pop_users_by_replies, trending_hashtags = trending_hashtags)

@app.route('/profile/<name>')
def profile(name):
    con = psycopg2.connect(dbname='twitter_lite', user='postgres', host='localhost', password='490023')
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    tweets_q = '''SELECT * 
                FROM tweets_withoutwords AS t
                WHERE user_name =''' + "\'" + name + "\'"
    
    cur.execute(tweets_q)

    tweets = cur.fetchall()

    con.commit()
    cur.close()

    # followers ='''SELECT u.name, count(*) as count
    #                         FROM user_map as u1, user_list_w_newid as u_dash1, graph_cb, 
    #                         WHERE u.oldid = user_list_w_newid.oldid AND user_list_w_newid.newid = 
    #                         GROUP BY u.name
    #                         ORDER BY n_replies desc
    #                         LIMIT 10'''

    

    con.close()
    return render_template("profile.html", name = name, tweets = tweets)


if __name__ == "__main__":
    
    app.run(debug=True)
    