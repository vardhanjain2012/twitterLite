import psycopg2, psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for
import signal
import sys

def signal_handler(sig, frame):
	con.close()
	print('You pressed Ctrl+C!')
	sys.exit(0)


# for Vardhan
# con = psycopg2.connect(dbname='twitter_lite', user='postgres', host='localhost', password='MANGO')
# app = Flask(__name__)

# for Ashish
# con = psycopg2.connect(dbname='assignment2', user='postgres', host='localhost', password='490023')
app = Flask(__name__)



@app.route('/')
def hello_world():
    return render_template("entry.html")

@app.route('/feed/<username>')
def feed(username):
    con = psycopg2.connect(dbname='assignment2', user='postgres', host='localhost', password='490023')
    cur = con.cursor()
    cur.execute("SELECT * FROM tweets_withoutwords WHERE user_name=%s", [username])
    items = cur.fetchall()
    cur.close()
    con.close()
    return render_template("feed.html", users=items)

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
                WHERE user_name = \'%s\'
                ORDER BY t.date desc, t.time desc
                '''%(name)
    
    cur.execute(tweets_q)

    tweets = cur.fetchall()

    con.commit()
    cur.close()

    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    followers_q = '''
                SELECT user_map.name as follower_name
                FROM 
                    (
                    SELECT user_list_w_newid.oldid AS follower_oldid
                    FROM
                        (
                        SELECT graph_cb.follower_newid AS follower_newid
                        FROM
                            (
                            SELECT user_list_w_newid.newid as newid
                            FROM
                                (
                                SELECT oldid 
                                FROM user_map
                                WHERE name = \'%s\'
                                ) AS foo,
                                user_list_w_newid
                            WHERE foo.oldid = user_list_w_newid.oldid
                            ) AS bar,
                            graph_cb
                        WHERE graph_cb.following_newid = bar.newid
                        ) as foobar1,
                        user_list_w_newid
                    WHERE foobar1.follower_newid = user_list_w_newid.newid
                    ) AS foobar2,
                    user_map
                WHERE user_map.oldid = follower_oldid
                ;
                ''' %(name)

    cur.execute(followers_q)

    followers = cur.fetchall()

    con.commit()
    cur.close()

    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    followings_q = '''
                SELECT user_map.name as following_name
                FROM 
                    (
                    SELECT user_list_w_newid.oldid AS following_oldid
                    FROM
                        (
                        SELECT graph_cb.following_newid AS following_newid
                        FROM
                            (
                            SELECT user_list_w_newid.newid as newid
                            FROM
                                (
                                SELECT oldid 
                                FROM user_map
                                WHERE name = \'%s\'
                                ) AS foo,
                                user_list_w_newid
                            WHERE foo.oldid = user_list_w_newid.oldid
                            ) AS bar,
                            graph_cb
                        WHERE graph_cb.follower_newid = bar.newid
                        ) as foobar1,
                        user_list_w_newid
                    WHERE foobar1.following_newid = user_list_w_newid.newid
                    ) AS foobar2,
                    user_map
                WHERE user_map.oldid = following_oldid
                ;
                ''' %(name)

    cur.execute(followings_q)

    followings = cur.fetchall()

    con.commit()
    cur.close()

    con.close()
    return render_template("profile.html", name = name, tweets = tweets, followers = followers, follower_count = len(followers), followings = followings, following_count = len(followings))


if __name__ == "__main__":
	# signal(signal.SIGINT, handler)
	app.run(debug=True)

