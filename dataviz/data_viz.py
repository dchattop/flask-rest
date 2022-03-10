import zipfile
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.backends.backend_pdf as pdf
import fetch_data
from config import config
import math, random, string
import os, sys


# l_functions = [func for func in dir(__dir__)]
# for i in dir():
# print(dir(__builtins__))
# if '_accnt' in dir(__builtins__):
#    print('ok')


# Generate unique names for file
def generate_name(file_path):
    fname_list = [fname.split('.')[0] for fname in os.listdir(file_path) if os.path.isdir(fname) == False]
    gen_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
    if gen_name not in fname_list:
        return file_path + '/' + gen_name
    else:
        try:
            generate_name(file_path)
        except RecursionError as re:
            print("Unique Files cannot be created. All possible names exhausted")
            return "Error"


# Save Viz in pdf
def save_viz_pdf(filename):
    pp = pdf.PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(pp, format='pdf', bbox_inches='tight')
        plt.close()
    pp.close()
    return filename


# viz code for account sql
def _accnt(data):
    if data == [{'error': 'Error while fetching data'}] or data == [{"data": "Not Found"}]:
        return data
    df = pd.DataFrame(data)
    df1 = df[["billing_country", "annual_revenue"]].fillna(0)
    #df2 = df1.set_index('account_id')
    df2 = df1.groupby(['billing_country']).sum()
    low = df2.min()
    high = df2.max()
    #df_viz_pie = df2.plot.pie(y='annual_revenue', figsize=(10, 5), ylabel='', fontsize=12, autopct=lambda x: f'{round(x * df2.sum()[0] / 100)}' if x != 0 else '')
    df_viz_bar = df2.plot.bar(y=0, ylabel='account_revenue', figsize=(10, 5), ylim=[0, math.ceil(high + 0.2 * (high - low))])
    #df_viz_pie.set_title('Revenue', fontsize=20)
    df_viz_bar.set_title('Revenue', fontsize=20)
    # df_figure_pie = df_viz_pie.legend(df1['account_id'], bbox_to_anchor=(1.1, 1), loc="best").get_figure()
    # df_figure_bar = df_viz_bar.legend(df1['account_id'], bbox_to_anchor=(1.1, 1), loc="best").get_figure()
    #df_viz_bar.legend(df1['billing_country'], bbox_to_anchor=(1.1, 1), loc="best")
    # bar_file = f'{generate_name(config.project_temp)}.jpg'
    # df_figure_pie.savefig(f'{config.project_home}/temp/pie.jpg', bbox_inches='tight')
    # df_figure_bar.savefig(f'{bar_file}', bbox_inches='tight')
    pdf_file = f'{generate_name(config.project_temp)}.pdf'
    return save_viz_pdf(pdf_file)


def _leadmngmnt(data):
    if data == [{'error': 'Error while fetching data'}] or data == [{"data": "Not Found"}]:
        return data
    df = pd.DataFrame(data)
    df = df[['super_region', 'lead_id']]
    df_sub = df.groupby(['super_region']).count().reset_index()
    # df_sub = df_sub[df['super_region'] != '0']
    low = df_sub.min()[1]
    high = df_sub.max()[1]
    df_viz_bar = df_sub.plot.bar(y=1, x=0, ylabel='lead_id', figsize=(10, 5),
                                 ylim=[0, math.ceil(high + 0.2 * (high - low))])
    df_viz_pie = df_sub.plot.pie(y=1, ylabel='', figsize=(20, 10), labels=df_sub['super_region'],
                                 autopct=lambda x: f'{round(x * df_sub.sum()[1] / 100)}')
    df_viz_pie.set_title('Lead Management', fontsize=20)
    df_viz_bar.set_title('Lead Management', fontsize=20)
    pdf_file = f'{generate_name(config.project_temp)}.pdf'
    return save_viz_pdf(pdf_file)


# Fetch data and Create list of visualisation in form of pdfs and zip for each API/SQL
# Note: To visualise data code needs to be added to this file as a function like above e.g. of _leadmngmnt or _accnt
def generate_charts(sql_file_list):
    created_file = []
    for i in sql_file_list:
        viz_func = '_' + i.replace('-', '_').split('.')[0]
        if viz_func in l_functions:
            created_file.append(eval(viz_func)(fetch_data.fetch_data(i.split('.')[0])))
            # created_file.append(_accnt(fetch_data.fetch_data(i.split('.')[0])))
    not_aFile = False
    if len(created_file) > 1:
        zip_file = f'{generate_name(config.project_temp)}.zip'.split('/')[-1]
        with zipfile.ZipFile(f'{config.project_temp}/{zip_file}', 'w') as zm:
            for file in created_file:
                if file is not None and os.path.isfile(str(file)) == True and file is not list:
                    zm.write(file, compress_type=zipfile.ZIP_DEFLATED, arcname=file.split('/')[-1])
                else:
                    not_aFile = True
        if not not_aFile:
            return f'{config.project_temp}/{zip_file}'
        else:
            return created_file[0]
    else:
        return created_file[0]


l_functions = dir()
