import pandas as pd
import requests
import json

url = 'https://<server>/api/v2/intelligence/?username='
username = '<username>'
api_key = '<api key>'
start_date_time = '2019-04-01T00:00:00.000Z'
end_date_time = '2019-04-30T23:59:59.999Z'
filename = 'Initial_Indicators_April_2019.csv'

start_num = str(0) #variable to set update_id__gt=0
apiCall = url+username+'&api_key='+api_key+'&created_ts__gte='+start_date_time+'&created_ts__lte='+end_date_time+'&update_id__gt='+start_num+'&order_by=update_id&limit=10000'
response = requests.get(apiCall) #Define response
data = json.loads(response.text) #Load the json data
values = data["objects"] #Convert to objects
df = pd.DataFrame.from_dict(values, orient="columns") #Create pandas dataframe from data objects
df = df.sort_values('update_id').reset_index(drop=True)
new_max_update_id = str(df['update_id'].iloc[-1] + 1) #Find the last update_id and add 1 for a starting place in next api call
while True: #Run until the length of df2 is less than 1000
    try: 
        print (len(df))
        apiCall = url+username+'&api_key='+api_key+'&created_ts__gte='+start_date_time+'&created_ts__lte='+end_date_time+'&update_id__gt='+new_max_update_id+'&order_by=update_id&limit=10000'
        response = requests.get(apiCall, verify=False)
        data = json.loads(response.text)
        values = data["objects"]
        df2 = pd.DataFrame.from_dict(values, orient="columns") #Convert new data to dataframe
        df2 = df2.sort_values('update_id').reset_index(drop=True)
        df = df.append(df2, ignore_index=True) #Add new data to df
        new_max_update_id = str(df2['update_id'].iloc[-1] + 1) #Update starting point for next api call
    except:
        if len(df2) < 1000:
            break
