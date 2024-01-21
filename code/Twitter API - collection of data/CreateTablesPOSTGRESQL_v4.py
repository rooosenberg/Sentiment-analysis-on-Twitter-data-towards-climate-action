#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:27:15 2020
@author: carlotatarazonalizarraga
"""

import tweepy
import json
import pandas as pd
import csv
import time
import mysql.connector
from psycopg2 import Error
import psycopg2

#imports for catching the errors
from ssl import SSLError
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError

#IMPORT 2 FILES WITH TWITTER API CREDENTIALS, DB CREDS AND SEARCH PARAMETERS

import database_credsSDG as db_creds

#SCHEMA AND TABLES NAMES
schema = 'twitter'
table_name_POSTS = 'posts'
table_name_USERS = 'users'



## ****** LOAD POSTGRESQL DATABASE ***** ##
def connect_db_p ():
    # Set up a connection to the postgres server.
    conn_string = "host="+ db_creds.PGHOST +" port="+ "5432" +" dbname="+ db_creds.PGDATABASE +" user=" + db_creds.PGUSER +" password="+ db_creds.PGPASSWORD
    conn=psycopg2.connect(conn_string)

    return conn

#### CREATE THE TABLES ####
def create_tables(schema,table_name_POSTS,table_name_USERS):

    
    con = connect_db_p()
    cursor = con.cursor()

    try:

        if con.closed == 0:


            query_create_users = 'CREATE TABLE {}.{} (user_id bigint NOT NULL,tweet_id bigint,user_name character varying COLLATE pg_catalog."default",user_loc character varying COLLATE pg_catalog."default",user_follow_count bigint,user_friends_count bigint,user_fav_count bigint,user_status_count bigint,verified boolean)'.format(schema, table_name_USERS)
            cursor.execute(query_create_users)

            query_create_posts = 'CREATE TABLE {}.{} (tweet_id bigint NOT NULL,user_id bigint NOT NULL,text character varying COLLATE pg_catalog."default",sourc character varying COLLATE pg_catalog."default",lang character varying COLLATE pg_catalog."default",created_date timestamp without time zone,week_of_year bigint,day_of_year bigint,month bigint,year bigint, place_id character varying,place_name character varying,coord point,reply_id bigint,reply_user_id bigint,retweet_id bigint,retweet_user_id bigint,quote_id bigint,	quote_user_id bigint,reply_count bigint,retweet_count bigint,favorite_count bigint,quote_count bigint,hashtags character varying COLLATE pg_catalog."default", mention_ids character varying COLLATE pg_catalog."default")'.format(schema, table_name_POSTS)
            cursor.execute(query_create_posts)
            con.commit()
            print('Tables created')
    except Error as e:
        print(e)

    cursor.close()
    con.close()
    return


#Call the function to create the tables
create_tables(schema,table_name_POSTS,table_name_USERS)
