import os
from dateutil import parser
import googleapiclient.discovery
import pandas as pd
import isodate

# Data viz packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# NLP
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

#import funtions
import get_channel_stats as gcs
import get_video_ids as gvi
import get_video_details as gvd


yt_api_key = os.environ['yt_api_key']
channel_ids = ["UCYJ61XIK64sp6ZFFS8sctxw",
                #more channels
]

api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client
youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey=yt_api_key)

playlist_id = "UUYJ61XIK64sp6ZFFS8sctxw"
# Get video IDs
video_ids = gvi.get_video_ids(youtube, playlist_id)
# Get video details
video_df = gvd.get_video_details(youtube, video_ids)
# Check for NULL values
video_df.isnull().any()
# Convert count columns to numeric
numeric_cols = ['viewCount', 'likeCount', 'favouriteCount', 'commentCount']
video_df[numeric_cols] = video_df[numeric_cols].apply(pd.to_numeric, errors = 'coerce', axis = 1)
# Publish day in the week
video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: parser.parse(x)) 
video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A")) 
# convert duration to seconds
video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]')
# Add tag count
video_df['tagCount'] = video_df['tags'].apply(lambda x: 0 if x is None else len(x))

day_df = pd.DataFrame(video_df['pushblishDayName'].value_counts())
weekdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_df = day_df.reindex(weekdays)
ax = day_df.reset_index().plot.bar(x='index', y='pushblishDayName', rot=0)
plt.show()