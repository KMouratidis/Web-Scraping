import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# utility to create a name string from a dictionary
def name_joiner(x):
    return " ".join(v for k,v in x.items())

# utility to clean dates
replace = lambda x: re.sub("--", "-",re.sub("\s", "-", x[0].strip() if len(x) else " "))


## PLAYER DATA
url = "http://www.pgatour.com/data/r/stats/current/02671.json"
resp = requests.get(url)
json_str = json.loads(resp.text)
json_str = json_str["tours"][0]['years'][0]['stats'][0]['details']

df = pd.DataFrame(json_str)
df['statValue1'] = df['statValues'].apply(lambda x: x['statValue1'])
df['statValue2'] = df['statValues'].apply(lambda x: x['statValue2'])
df['statValue3'] = df['statValues'].apply(lambda x: x['statValue3'])
df['statValue4'] = df['statValues'].apply(lambda x: x['statValue4'])
df['statValue5'] = df['statValues'].apply(lambda x: x['statValue5'])
df['rndEvents'] = df['statValues'].apply(lambda x: x['rndEvents'])
df["name"] = df["plrName"].apply(name_joiner)

df.drop(['plrName', 'statValues'], axis=1, inplace=True)


## Scorecards
url2 = "http://www.pgatour.com/data/r/current/schedule.json"
resp2 = requests.get(url2)
json_str2 = json.loads(resp2.text)

df2 = pd.DataFrame(json_str2['tours'][0]['trns'])
# champions
df2['FedExCupWinnerShare'] = df2['champions'].apply(lambda x: x[0].get('FedExCupWinnerShare'))
df2['isMember'] = df2['champions'].apply(lambda x: x[0]['isMember'])
df2['playerName'] = df2['champions'].apply(lambda x: x[0]['playerName'])
df2['plrNum'] = df2['champions'].apply(lambda x: x[0]['plrNum'])
df2['winningShare'] = df2['champions'].apply(lambda x: x[0]['winningShare'])
# course
df2['courseName'] = df2['courses'].apply(lambda x: x[0].get('courseName'))
df2['host'] = df2['courses'].apply(lambda x: x[0]['host'])
df2['isTpc'] = df2['courses'].apply(lambda x: x[0]['isTpc'])
df2['number'] = df2['courses'].apply(lambda x: x[0]['number'])
df2['rank'] = df2['courses'].apply(lambda x: x[0]['rank'])
# date
df2['start'] = df2['date'].apply(lambda x: x['start'])
df2['end'] = df2['date'].apply(lambda x: x['end'])
df2['weekNumber'] = df2['date'].apply(lambda x: x['weekNumber'])
# subEvents
df2['subEvents'] = df2['subEvents'].apply(replace)
# trnName
df2['trnName'] = df2['trnName'].apply(lambda x: x['official'])
# playerName
df2["playerName"] = df2["playerName"].apply(func)

df2.drop(["date","courses", "champions", "links"], axis=1, inplace=True)
