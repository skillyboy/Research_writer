import pandas as pd
import gzip
import json
import statistics

path = ('Video_Games_5.json.gz')

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield json.loads(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

# Call getDF function and store result in a variable
df = getDF(path)

# Print the dataframe
print(df)
print(df.shape)
print(df.columns)

ratings = []
with gzip.open(path, 'rb') as f:
    for line in f:
        review = json.loads(line)
        ratings.append(review['overall'])

avg_rating = statistics.mean(ratings)
print(f"Average rating: {avg_rating:.2f}")



# print(df.nunique())
# print(df.dtypes)
# print(df.isnull().sum())
# print(df.describe())
# print(df['overall'].value_counts())



