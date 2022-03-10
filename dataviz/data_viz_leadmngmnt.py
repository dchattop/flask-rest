#import matplotlib.pyplot as plt
import requests
import json
import pandas as pd

url = "http://127.0.0.1:5000/customsql"

payload = json.dumps({
  "sql": "select distinct EXTRACT(year from c.created_date_est) year_month, d.super_region,d.sub_region,d.region, case when lead_stage_to in ('Marketing Rejected','Sales Rejected','Marketing Disqualified','Sales Disqualified') and rejection_reason='Small Purchase' then 'Rejected Leads - Small Purchase'  when lead_stage_to in ('Marketing Disqualified','Sales Disqualified')  then 'Disqualified Leads' when lead_stage_to in ('Marketing Rejected','Sales Rejected','Marketing Disqualified','Sales Disqualified') then 'Rejected Leads' when lead_stage_to in ('Marketing Accepted','Sales Accepted') then 'Accepted Leads' END as Lead_Type, c.lead_id from  APL_VDB_SFDC_SALES.sfdc_lead_mngmnt_hist c full outer join APL_VDB_SFDC_SALES.sfdc_lead d on c.lead_id=d.lead_id"
})
headers = {
  'Content-Type': 'application/json',
  'Connection': 'keep-alive',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

response = requests.request("GET", url, headers=headers)

print(response.json())
df_json=response.json()
df = pd.DataFrame.from_dict(df_json)
#print(df)
df_sub = df.groupby(['super_region']).count()
df_figure=df_sub.plot(kind='pie', y='lead_id',ylabel='', figsize=(20, 10),autopct=lambda x: f'{round(x*df_figure.sum()[1]/100)}').legend(loc=2).get_figure()
df_figure.savefig('C:/Users/amaheswa/Documents/flask-project/poc1/flask-rest/temp/test1.png')
# df1 = df[["account_id", "annual_revenue"]].fillna(0)
# #print(df1)
# df2 = df1.set_index('account_id')
# df_viz=df2.plot.pie(y='annual_revenue', figsize=(10, 5), ylabel='', fontsize=12, startangle=0)
# df_viz.set_title('Revenue', fontsize=20)
# df_figure=df_viz.legend(df1['account_id'],bbox_to_anchor=(1.1,1), loc="best").get_figure()
# df_figure.savefig('C:/Users/amaheswa/Documents/flask-project/poc1/flask-rest/temp/test.png')
#print(response.text)
#print(json.loads(response.text))