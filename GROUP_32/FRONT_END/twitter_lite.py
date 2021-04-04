import psycopg2, psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for
import sys
import time


dbname = 'group_32'
host = '10.17.10.70'
password = 'rdbm5OZCxcpS9'
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("entry.html")

@app.route('/feed/<name>')
def feed(name):
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    tweets_q = '''SELECT * 
				FROM (SELECT user_map.name as following_name
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
					WHERE user_map.oldid = following_oldid) AS p, 
				tweets_withoutwords AS t
                WHERE t.user_name = following_name
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
    return render_template("feed.html", name = name, tweets = tweets, followers = followers, follower_count = len(followers), followings = followings, following_count = len(followings))

@app.route('/handle_data_signup', methods=['POST'])
def handle_data_signup():
    name = request.form['uname']
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    countUsername ='''SELECT COUNT(*) as count
                            FROM user_map 
                            WHERE name = %s'''
    cur.execute(countUsername, [name])
    numUsernames = cur.fetchall()[0][0]
    cur.close()
    con.close()
    if numUsernames==1:
        return render_template("entry.html", message="Username not available, signup again with a new one!")
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    maxid ='''SELECT MAX(oldid) as maxid
                            FROM user_map'''
    cur.execute(maxid)
    maxoldid = cur.fetchall()[0][0]
    cur.close()
    con.close()
    print(maxoldid)
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    maxid ='''SELECT MAX(newid) as maxid
                            FROM user_list_w_newid'''
    cur.execute(maxid)
    maxnewid = cur.fetchall()[0][0]
    cur.close()
    con.close()
    print(maxnewid)

    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    insertOne ='''INSERT INTO user_map(oldid, name) VALUES(%s, %s)'''
    cur.execute(insertOne, [maxoldid+1, name])
    con.commit()
    cur.close()
    con.close()

    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    insertOne ='''INSERT INTO user_list_w_newid(newid, oldid) VALUES(%s, %s)'''
    cur.execute(insertOne, [maxnewid+1, maxoldid+1])
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('feed', name=name))

@app.route('/handle_data_login', methods=['POST'])
def handle_data_login():
    name = request.form['uname']
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    countUsername ='''SELECT COUNT(*) as count
                            FROM user_map 
                            WHERE name = %s'''
    cur.execute(countUsername, [name])
    numUsernames = cur.fetchall()[0][0]
    cur.close()
    con.close()
    if numUsernames==0:
        return render_template("entry.html", message="Invalid username, try again!")
    return redirect(url_for('feed', name=name))

#TODO: make it posonalized for user and use tweet times
@app.route('/explore')
def explore():
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
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
                            FROM tweets_withoutwords) AS foo
                        WHERE link_types[s] = 'hashtag'
                        GROUP BY links[s]
                        ORDER BY count desc
                        LIMIT 100'''

    cur.execute(trending_hashtags_q)

    trending_hashtags = cur.fetchall()

    con.commit()
	
    cur.close()
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    tweets_q = '''SELECT * 
				FROM (SELECT reply_to_tweet as f, COUNT(*) 
					FROM tweets_withoutwords AS t
					GROUP BY reply_to_tweet
					ORDER BY COUNT(*) DESC
					LIMIT 100) as foo, tweets_withoutwords AS t
				WHERE foo.f=t.id
				ORDER BY count DESC, t.date desc, t.time desc
                '''
	
    cur.execute(tweets_q)

    tweets = cur.fetchall()

    con.commit()
    cur.close()
	
    con.close()
  
    return render_template("explore.html", tweets = tweets, pop_users_by_replies = pop_users_by_replies, trending_hashtags = trending_hashtags)

@app.route('/profile/<name>/<viewer>')
def profile(name, viewer):
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
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
                ''' %(viewer)

    cur.execute(followings_q)

    followingsViewer = cur.fetchall()

    con.commit()
    cur.close()

    con.close()

    print(followingsViewer)

    isPresent = False
    if([name] in followingsViewer):
        isPresent=True
    return render_template("profile.html", name = name, tweets = tweets, followers = followers, follower_count = len(followers), followings = followings, following_count = len(followings), viewer=viewer, isPresent=isPresent)

@app.route('/handle_follow/<name>/<viewer>')
def handle_follow(name, viewer):
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    insertOne ='''INSERT INTO graph_cb(follower_newid, following_newid, timestamp) VALUES(
        (SELECT newid 
        FROM user_list_w_newid NATURAL JOIN user_map
        WHERE user_map.name=%s), 
        (SELECT newid 
        FROM user_list_w_newid NATURAL JOIN user_map
        WHERE user_map.name=%s), %s)'''
    ts = time.time()
    cur.execute(insertOne, [viewer, name, int(ts)])
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('profile', name=name, viewer=viewer))

@app.route('/handle_unfollow/<name>/<viewer>')
def handle_unfollow(name, viewer):
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor()
    removeOne ='''DELETE FROM graph_cb WHERE
        (follower_newid=(SELECT newid 
        FROM user_list_w_newid NATURAL JOIN user_map
        WHERE user_map.name=%s)) AND
        (following_newid=(SELECT newid 
        FROM user_list_w_newid NATURAL JOIN user_map
        WHERE user_map.name=%s))'''
    cur.execute(removeOne, [viewer, name])
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('profile', name=name, viewer=viewer))

@app.route('/trend/<hash>')
def trend(hash):
    con = psycopg2.connect(dbname=dbname, user='postgres', host=host, password=password)
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("testing", hash)
    tweets_q = '''SELECT *
					FROM
					(SELECT *,generate_subscripts(link_types, 1) AS s
						FROM tweets_withoutwords) AS foo
					WHERE link_types[s] = 'hashtag' AND links[s]=\'%s\'
					ORDER BY foo.date desc, foo.time desc
                '''%("/search?q=%23"+hash)
    
    cur.execute(tweets_q)

    tweets = cur.fetchall()
	
    con.commit()
    cur.close()

    con.close()
    return render_template("trending.html", tweets = tweets)
    

if __name__ == "__main__":
	app.run()