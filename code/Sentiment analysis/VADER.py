
"""
VADER

The sentiment score range between -1 to 1 for the whole sentence and -4 to 4 for the each word. The normalized sum gives the total score (therefore it works with the different ranges). The total score is presented as *compound*. The *positive*, *negative* and *neutral* is the ratios for proportions of text that fall in each category (therefore range between 0 and 1).

IMPORTANTLY: these proportions represent the "raw categorization" of each lexical item (e.g., words, emoticons/emojis, or initialisms) into positve, negative, or neutral classes; they do not account for the VADER rule-based enhancements such as word-order sensitivity for sentiment-laden multi-word phrases, degree modifiers, word-shape amplifiers, punctuation amplifiers, negation polarity switches, or contrastive conjunction sensitivity

Source: https://github.com/cjhutto/vaderSentiment

Date: 2021-09-06

Auther: emeros
"""
# ---------------------------------------------------------------------------------------------------------------------------------

import pandas as pd

import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------------------------------------------------------------------------------------------------------------------------

#df = pd.read_csv (r'C:\Users\Emelie\Documents\Exjobb\Twitter_API_data\data\all_data_non_dub.csv', dtype={'quote_count':int, 'favorite_count':int, 'retweet_count':int})
df = pd.read_csv (r'C:\Users\Emelie\Documents\Exjobb\Twitter_API_data\data\all_data_non_dub.csv')

df = df[df['Tweet'].notna()]

analyzer = SentimentIntensityAnalyzer()

# calculate score for each tweet
scores = []
for i in df['Tweet']:
    compound = analyzer.polarity_scores(i)["compound"]
    pos = analyzer.polarity_scores(i)["pos"]
    neu = analyzer.polarity_scores(i)["neu"]
    neg = analyzer.polarity_scores(i)["neg"]

    scores.append({"Compound": compound,
                       "Positive": pos,
                       "Negative": neg,
                       "Neutral": neu
                  })

# create df from all scores
df_sentiments_score = pd.DataFrame.from_dict(scores)

com_sent = []
# sort each tweet accordingly to threshold given by VADER paper
for i in df_sentiments_score['Compound']:
    if i >= 0.05:
        com_sent.append('positive')
    elif i <= -0.05:
        com_sent.append('negative')
    else:
        com_sent.append('neutral')

# adding type of sentiment to df
df_sentiments_score['sentiment'] = com_sent

#put the sentiment score and sentiment togheter with the large df
df_sentiments_score = pd.concat([df, df_sentiments_score], axis=1)

#save it
df_sentiments_score.to_csv (r'C:\Users\Emelie\Documents\Exjobb\Twitter_API_data\data\all_data_VADER.csv')
