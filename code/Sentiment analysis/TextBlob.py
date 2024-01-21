
import pandas as pd
from textblob import TextBlob

# -----------------------------------------------------------------------------------------------------------

df = pd.read_csv (r'C:\Users\Emelie\Documents\Exjobb\Twitter_API_data\data\all_data_VADER.csv')
df = df[df['Tweet'].notna()]

scores = []
for i in df['Tweet']:
    text = TextBlob(i)
    sentiment = text.sentiment

    scores.append({"Polarity": sentiment[0],
                       "Subjectivity": sentiment[1],
                  })

# create df
df_sentiments_score = pd.DataFrame.from_dict(scores)

# put it togheter with large df
df_sentiments_score = pd.concat([df, df_sentiments_score], axis=1)

# save it
df_sentiments_score.to_csv (r'C:\Users\Emelie\Documents\Exjobb\Twitter_API_data\data\all_data_TextBlob.csv')
