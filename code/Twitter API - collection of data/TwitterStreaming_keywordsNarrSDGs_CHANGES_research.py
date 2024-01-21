#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 09:35:38 2020
@author: carlotatarazonalizarraga
"""

import sys
import os

import tweepy
import json
import pandas as pd
import csv
import time
import mysql.connector
from mysql.connector import Error
import datetime
import psycopg2

#imports for catching the errors
from ssl import SSLError
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError

#IMPORT 2 FILES WITH TWITTER API CREDENTIALS, DB CREDS AND SEARCH PARAMETERS
import twitterAPI_credsSDG as tw_creds
import database_credsSDG as db_creds
import search_parametersNarrSDGs as s_params


##SEARCH PARAMETERS FROM THE FILE
#Definicion palabras claves busqueda
keywords = s_params.keywords
ub_name='None'

table_name_POSTS = 'posts'
table_name_USERS = 'users'

"""
Filtra primero por keywords y luego hace check de la ubicacion (usuario y tweet)
"""


## ****** LOAD POSTGRESQL DATABASE ***** ##
def connect_db_p ():
    # Set up a connection to the postgres server.
    conn_string = "host="+ db_creds.PGHOST +" port="+ "5432" +" dbname="+ db_creds.PGDATABASE +" user=" + db_creds.PGUSER +" password="+ db_creds.PGPASSWORD
    conn=psycopg2.connect(conn_string)

    return conn



##ADD KEYWORKDS
#### Call the connect_db_p() and insert into the tables
def connect(user_id,
            user_name,
            user_location,
            user_follow_count,
            user_friends_count,
            user_fav_count,
            user_status_count,
            verified,
            tweet_id,
            text,
            source,
            language,

            keywords_db,

            created_date,
            week,
            day_of_year,
            month,
            year,

            place_id,
            place_name,
            coord,
            reply_id, reply_user_id,
            retweet_id,retweet_user_id,
            quote_id,quote_user_id,
            reply_count,retweet_count,favorite_count,quote_count,
            hashtags, mention_ids):

    #Con la conexion llamando a la funcion se crea el cursor
    con = connect_db_p()
    cursor = con.cursor()
    schema = 'twitter'
    #table_name_POSTS = 'posts'
    #table_name_USERS = 'users'
    try:

        if con.closed == 0:


            query = "INSERT INTO {}.{} (user_id,tweet_id,user_name,user_loc,user_follow_count,user_friends_count,user_fav_count,user_status_count,verified) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s)".format(schema, table_name_USERS)
            cursor.execute(query, (user_id,
                                    tweet_id,
                                    user_name,
                                    user_location,
                                    user_follow_count,
                                    user_friends_count,
                                    user_fav_count,
                                    user_status_count,
                                    verified
                                  )
                          )

##ADD KEYWORKDS

            query2 = "INSERT INTO {}.{} (tweet_id, user_id,text,sourc,lang,created_date,week_of_year,day_of_year,month,year, place_id,place_name,coord,reply_id,reply_user_id,retweet_id,retweet_user_id,quote_id,quote_user_id,reply_count,retweet_count,favorite_count,quote_count,hashtags,mention_ids,keywords) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)".format(schema, table_name_POSTS)
##ADD KEYWORKDS

            cursor.execute(query2, (tweet_id,
                                   user_id,
                                   text,
                                   source,
                                   language,
                                   created_date,
                                   week,
                                   day_of_year,
                                   month,
                                   year,
                                   place_id,
                                   place_name,
                                   coord,
                                   reply_id,
                                   reply_user_id,
                                   retweet_id,
                                   retweet_user_id,
                                   quote_id,
                                   quote_user_id,
                                   reply_count,
                                   retweet_count,
                                   favorite_count,
                                   quote_count,
                                   hashtags,
                                   mention_ids,
                                   keywords_db
                                  )
                          )


            con.commit()
            #print('tweet guardado')
    except Error as e:
        print(e)
        print(text)


    cursor.close()
    con.close()
    return


class MyStreamListener(tweepy.StreamListener):
    def on_data(self,data):
        # Twitter returns data in JSON format - we need to decode it first
        try:
            decoded = json.loads(data)
        except:
            print ("Error on_data: %s" % str(e)) #we don't want the listener to stop

            return True


        #DATE METADATA
        created_at = decoded.get('created_at') #Fecha en string


        created_date = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y').date() #timestamp

        week = created_date.isocalendar()[1]
        day_of_year = int(created_date.strftime('%j'))
        month = created_date.month
        year = created_date.year


        #LOCATION METADATA

        #En caso de estar geolocalizado guardar la geolocalizacion
        #Si esta geolocalizado dentro de un bounding box (no exacta)

        if decoded.get('place') is not None:
            place_id = decoded.get('place').get('id')
            place_name =decoded.get('place').get('name')
        else:
            place_id = None
            place_name = None


        #Si es localizacion exacta
        #Geo is deprecated, they suggest to use simply coordinates
        if decoded.get('coordinates') is not None:
            m_coord = decoded.get('coordinates')['coordinates']
            coord='('+str(m_coord[0])+','+str(m_coord[1])+')'

        else:
        	coord = None


        #######USER METADATA
        user_name = '@' + decoded.get('user').get('screen_name') #nombre cuenta @itdUPM
        user_id=decoded.get('user').get('id') #id de la cuenta (int)

        if decoded.get('user').get('location'):
        	user_location = decoded.get('user').get('location')
        else:
        	user_location = 'None'


        user_follow_count=decoded.get('user').get('followers_count')
        user_friends_count=decoded.get('user').get('friends_count')
        user_fav_count=decoded.get('user').get('favourites_count')
        user_status_count=decoded.get('user').get('statuses_count')
        verified = decoded.get('user').get('verified')


        #TWEET METADATA
        tweet_id = decoded['id'] #tweet id (int64)
        language = decoded.get('user').get('lang')
        source = decoded['source'] #string source (web client, android, iphone) interesante???

        #############TEXT METADATA#########################

        if decoded.get('truncated'):
        	text = decoded['extended_tweet']['full_text'].replace('\n',' ')
        else:
        	text = decoded['text'].replace('\n',' ')


        #Checking the keywords in each tweet


        keywords_db =[]

        keywords = s_params.keywords

        for kw in keywords:
            if kw in text.lower():
                keywords_db.append(kw)






        #REPLY METADATA
        reply_id=decoded['in_reply_to_status_id']
        reply_user_id=decoded['in_reply_to_user_id']

        #RETWEET
        if decoded.get('retweeted_status') is not None:
            retweet_id = decoded['retweeted_status'] ['id']
            retweet_user_id = decoded['retweeted_status']['user']['id']

            if decoded['retweeted_status']['truncated']:
                text = decoded['retweeted_status']['extended_tweet']['full_text'].replace('\n',' ')
            else:
                text = decoded['retweeted_status']['text'].replace('\n',' ') #Contenido tweet


            reply_count = decoded['retweeted_status']['reply_count'] #Number of times this Tweet has been replied to
            retweet_count = decoded['retweeted_status']['retweet_count'] #Number of times this Tweet has been retweeted
            favorite_count = decoded['retweeted_status']['favorite_count'] #how many times this Tweet has been liked by Twitter users.
            quote_count = decoded['retweeted_status']['quote_count']



            hashtags_list=decoded['retweeted_status']['entities']['hashtags']
            mentions=decoded['retweeted_status']['entities']['user_mentions']

            hashtags=''
            c=0
            if len(hashtags_list)>0:
                for i in range(0, len(hashtags_list)-1):
                    mh=hashtags_list[i].get('text')
                    hashtags=hashtags+mh+';'
                    c=c+1
                mh=hashtags_list[c].get('text')
                hashtags=hashtags+str(mh)
            else:
                hashtags='None'

            mention_ids=''
            c=0
            if len(mentions)>0:
                for i in range(0, len(mentions)-1):
                    mid=mentions[i].get('id_str')
                    mention_ids=mention_ids+mid+';'#use a different separator!
                    c=c+1
                mid=mentions[c].get('id_str')
                mention_ids=mention_ids+str(mid)
            else:
                mention_ids='None'

            if decoded['retweeted_status']['is_quote_status']:
                if 'quoted_status' not in decoded['retweeted_status']:
                    quote_id=None
                    quote_user_id=None
                else:
                    quote_id=decoded['retweeted_status']['quoted_status']['id']
                    quote_user_id=decoded['retweeted_status']['quoted_status']['user']['id']
            else:
                quote_id=None
                quote_user_id=None

        else:

            reply_count = decoded['reply_count'] #Number of times this Tweet has been replied to
            retweet_count = decoded['retweet_count'] #Number of times this Tweet has been retweeted
            favorite_count = decoded['favorite_count'] #how many times this Tweet has been liked by Twitter users.
            quote_count = decoded['quote_count']
            retweet_id = None
            retweet_user_id = None

            if decoded['is_quote_status']:
                if 'quoted_status' not in decoded:
                    quote_id=None
                    quote_user_id=None
                else:
                    quote_id=decoded['quoted_status']['id']
                    quote_user_id=decoded['quoted_status']['user']['id']
            else:
                quote_id=None
                quote_user_id=None

            hashtags_list=decoded.get('entities').get('hashtags')
            mentions=decoded.get('entities').get('user_mentions')

            hashtags=''
            c=0
            if len(hashtags_list)>0:
                for i in range(0, len(hashtags_list)-1):
                    mh=hashtags_list[i].get('text')
                    hashtags=hashtags+mh+';'
                    c=c+1
                mh=hashtags_list[c].get('text')
                hashtags=hashtags+str(mh)
            else:
                hashtags='None'

            mention_ids=''
            c=0
            if len(mentions)>0:
                for i in range(0, len(mentions)-1):
                    mid=mentions[i].get('id_str')
                    mention_ids=mention_ids+mid+';'#use a different separator!
                    c=c+1
                mid=mentions[c].get('id_str')
                mention_ids=mention_ids+str(mid)
            else:
                mention_ids='None'


        #Si se ha proporcionado una ubicacion en search params
        if ub_name is not None:
            #Comprueba que este en el user_location o en el place_name del tweet (tweet localizado)
            #Si Madrid se encuentra en el place_name (geolocalizado)

            if (ub_name in str(place_name)) or (ub_name in str(user_location)):
                #print(mention_ids)
                connect(
                    #user data
                    user_id,
                    user_name,
                    user_location,
                    user_follow_count,
                    user_friends_count,
                    user_fav_count,
                    user_status_count,
                    verified,

                    tweet_id,
                    text,
                    source,
                    language,

                    keywords_db,

                    created_date,
                    week,
                    day_of_year,
                    month,
                    year,

                    place_id,
                    place_name,
                    coord,
                    reply_id, reply_user_id,
                    retweet_id,retweet_user_id,
                    quote_id,quote_user_id,
                    reply_count,retweet_count,favorite_count,quote_count,
                    hashtags,
                    mention_ids
                )
        #En ub_name (search parameters) no se ha indicado ubicacion --> se desea unicamente filtro keywords
        else:
            print('--')
            connect(
                    #user data
                    user_id,
                    user_name,
                    user_location,
                    user_follow_count,
                    user_friends_count,
                    user_fav_count,
                    user_status_count,
                    verified,

                    tweet_id,
                    text,
                    source,
                    language,

                    keywords_db,

                    created_date,
                    week,
                    day_of_year,
                    month,
                    year,

                    place_id,
                    place_name,
                    coord,
                    reply_id, reply_user_id,
                    retweet_id,retweet_user_id,
                    quote_id,quote_user_id,
                    reply_count,retweet_count,favorite_count,quote_count,
                    hashtags,
                    mention_ids
                )



        return True # keep stream alive

    def on_error(self, status_code):
        if status_code == 420:
            return True

        #   print 'paso por on_error\n'
        text_error = '---------------->An error has occured! Status code = %s at %s\n' % (status_code,datetime.datetime.now())
        #self.files.write_log (text_error)
        print (text_error)
        return True # keep stream alive

    def on_timeout(self):
        #   print 'paso por on_timeout\n'
        text_error = 'Snoozing Zzzzzz at %s\n' % ( datetime.datetime.now())
        #self.files.write_log (text_error)
        print (text_error)
        return False #restart streaming



def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)



if __name__ == '__main__':
    print ('Starting')
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(tw_creds.consumer_key, tw_creds.consumer_secret)
    auth.set_access_token(tw_creds.access_token, tw_creds.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=3, retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))

    #create the api and the stream object
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    #Filter the stream by keywords
    myStream.filter(track = keywords)
