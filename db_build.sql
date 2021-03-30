CREATE TABLE user_list_w_newid (
    newid int NOT NULL,
    oldid int NOT NULL,
    constraint user_list_w_newid_key primary key (newid),
    unique (oldid)
);

\copy user_list_w_newid from 'twitter_network/user_list_w_newid.txt' delimiter ' ';


CREATE TABLE user_map (
    oldid int NOT NULL,
    name text NOT NULL,
    constraint user_map_key primary key (oldid)
);

\copy user_map from 'twitter_network/user_map.txt' delimiter ' ';


CREATE TABLE graph_cb (
    follower_newid int NOT NULL,
    following_newid int NOT NULL,
    timestamp int NOT NULL,
    constraint graph_cb_key primary key (follower_newid, following_newid)
);

\copy graph_cb from 'twitter_network/graph_cb.txt' delimiter ' ';


CREATE TABLE wordtable (
    id int NOT NULL,
    unknown int NOT NULL,
    word text NOT NULL,
    constraint wordtable_key primary key (id),
    unique (word)
);

\copy wordtable from 'WordTable.txt';


CREATE TABLE tweets_withoutwords (
    user_name text NOT NULL,
    id bigint NOT NULL,
    date date NOT NULL,
    time time NOT NULL,
    via text NOT NULL,
    retweet_from text NOT NULL,
    reply_to_user text NOT NULL,
    reply_to_tweet text NOT NULL,
    content int [] NOT NULL,
    number_of_link_in_tweet int,
    link_types text [],
    links text [],
    constraint tweets_withoutwords_key primary key (id)
);

\copy tweets_withoutwords from 'Tweets-withoutwords/2010_10_14/tweet_result_0_cleaned.txt' delimiter ';';