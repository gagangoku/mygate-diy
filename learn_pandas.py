import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
}
df = pd.DataFrame(data, index=["day1", "day2", "day3"])
print (df)
print ('---')
print (df.loc["day2"])
print ('---')
print (df.loc["day2"][0])
print ('---')

print(pd.options.display.max_rows)
print ('---')

df = pd.read_csv('/tmp/1.csv', nrows=10)
print(df)
print ('---')
print(df.to_string())
print ('---')
print (df['pledge'])
print ('---')

data = {
  "Duration":{
    "0":60,
    "1":60,
    "2":60,
    "3":45,
    "4":45,
    "5":60
  },
  "Pulse":{
    "0":110,
    "1":117,
    "2":103,
    "3":109,
    "4":117,
    "5":102
  },
  "Maxpulse":{
    "0":130,
    "1":145,
    "2":135,
    "3":175,
    "4":148,
    "5":127
  },
  "Calories":{
    "0":409,
    "1":479,
    "2":340,
    "3":282,
    "4":406,
    "5":300
  }
}
df = pd.DataFrame(data)
print (df)
print ('---')

print(df.head(2))
print ('---')

print(df.info())
print ('---')


df = pd.read_csv('https://www.w3schools.com/python/pandas/dirtydata.csv')
print(df.info())
print ('---')
new_df = df.dropna()
print(new_df.to_string())
print ('---')

df.fillna(130, inplace=True)
print(df.to_string())
print ('---')
