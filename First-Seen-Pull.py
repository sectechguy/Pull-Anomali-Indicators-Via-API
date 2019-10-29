import pandas as pd
import requests
import json
from time import sleep
import math

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = 'https://<server>/api/v2/intelligence/?username='
username = '<username>'
api_key = '<api_key>'
WAIT_SECONDS = 5
BATCH_SLEEP_SECONDS = 300    

initial_indicators = pd.read_csv('/Capture_Indicators_Months_Jan_Feb_2019/initial_indicators.csv')
initial_list = initial_indicators['value'].tolist()
column1 = list()
column2 = list()
column3 = list()
column4 = list()
column5 = list()
for row in initial_list:
  value_api = url+username+'&api_key='+api_key+'&limit=10000&value='
  responses = requests.get(value_api+row, verify=False)
  data = json.loads(responses.text)
  valuess = data['objects']
  for index in valuess:
    column1.append(index['value'])
    column2.append(index['source'])
    column3.append(index['trusted_circle_ids'])
    column4.append(index['created_ts'])
    column5.append(index['tags'])
new__output = pd.DataFrame(
  {'Indicator': column1,
   'Source': column2,
   'Trusted Circle': column3,
   'Created': column4,
   'Tags': column5
  })

new__output.to_csv('Capture_Indicators_Months_Jan_Feb_2019/initial_with_others_first_seen.csv', header=True, index=False)
