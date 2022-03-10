import os, json
import pandas as pd
from utils.connect_db import fetch_resulset

#Fetch data based on sql files palced in sql folder
def fetch_data(filename):
    #print(filename)
    row_dict = '[{"data": "Not Found"}]'
    directory = './sql'
    full_filename = os.path.join(directory, filename+'.sql')
    if os.path.isfile(full_filename) and full_filename.endswith('.sql'):
        print(f"Running data fetch for : {full_filename}")
        with open(f'{full_filename}', 'r') as sq:
            query = sq.read().replace('\n', ' ')
        #query = query+" and super_region='APAC' LIMIT 10"
        #print(query)
        cols, rows = fetch_resulset(query)
        if cols == 'failed':
            error_d = '[{"error" : "Error while fetching data"}]'
            return json.loads(error_d)
        df = pd.DataFrame(rows, columns=cols)
        row_dict = json.dumps(json.loads(df.to_json(orient='records')))
        #print(row_dict)
        return json.loads(row_dict)
    else:
        return json.loads(row_dict)


#fetch custom sql data
def fetch_data_custom(data):
    query = data[list(data)[0]]
    cols, rows = fetch_resulset(query)
    if cols == 'failed':
        error_d = '[{"error" : "Error while fetching data"}]'
        # return rows
        return json.loads(error_d)
    df = pd.DataFrame(rows, columns=cols)
    row_dict = df.to_json(orient='records')
    return row_dict
