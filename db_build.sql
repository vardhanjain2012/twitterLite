CREATE TABLE user_list_w_newid (
    newid bigint NOT NULL,
    oldid bigint NOT NULL,
    constraint user_list_w_newid_key primary key (newid),
    unique (oldid)
);

\copy user_list_w_newid from 'data_dump/twitter_network/user_list_w_newid.txt' delimiter ' ';


CREATE TABLE user_map (
    oldid bigint NOT NULL,
    name text NOT NULL,
    constraint user_map_key primary key (oldid)
    unique(oldid)
);

\copy user_map from 'data_dump/twitter_network/user_map.txt' delimiter ' ';


CREATE TABLE graph_cb (
    follower_newid bigint NOT NULL,
    following_newid bigint NOT NULL,
    timestamp bigint NOT NULL,
    constraint graph_cb_key primary key (follower_newid, following_newid)
);

\copy graph_cb from 'data_dump/twitter_network/graph_cb.txt' delimiter ' ';


CREATE TABLE wordtable (
    id bigint NOT NULL,
    unknown bigint NOT NULL,
    word text NOT NULL,
    constraint wordtable_key primary key (id),
    unique (word)
);

\copy wordtable from 'data_dump/WordTable.txt';


CREATE TABLE tweets_withoutwords_staging (
    user_name text NOT NULL,
    id bigint NOT NULL, 
    date date NOT NULL,
    time time NOT NULL,
    via text NOT NULL,
    retweet_from text NOT NULL,
    reply_to_user text NOT NULL,
    reply_to_tweet bigint NOT NULL,
    content bigint [] NOT NULL,
    number_of_link_in_tweet bigint,
    link_types text [],
    links text []
);

\copy tweets_withoutwords_staging from 'data_dump/Tweets-withoutwords/2010_10_14/tweet_result_0_cleaned.txt';

CREATE TABLE tweets_withoutwords (
    user_name text NOT NULL,
    id bigint NOT NULL,
    date date NOT NULL,
    time time NOT NULL,
    via text NOT NULL,
    retweet_from text NOT NULL,
    reply_to_user text NOT NULL,
    reply_to_tweet bigint NOT NULL,
    content bigint [] NOT NULL,
    number_of_link_in_tweet bigint,
    link_types text [],
    links text [],
    constraint tweets_withoutwords_key primary key (id)
);

INSERT INTO tweets_withoutwords
    SELECT *
    FROM tweets_withoutwords_staging
ON CONFLICT DO NOTHING
;

DROP TABLE tweets_withoutwords_staging;
