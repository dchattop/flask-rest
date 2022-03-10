import os, json, flask
from flask import Flask, request, render_template
from flask_restful import Resource, Api
import pandas as pd
from fetch_data import fetch_data, fetch_data_custom
from dataviz.data_viz import generate_charts
from config import config

app = Flask(__name__)
api = Api(app)


# custom_sql_args = reqparse.RequestParser()
# custom_sql_args.add_argument("sql", type=str, help="Send SQL Query", required=True)

@app.route('/')
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/list_api")
def list_api_page():
    return render_template('list_api.html', api_list_items=[fname.split('.')[0] for fname in os.listdir(config.project_sql) if os.path.isdir(fname) == False])


@app.route("/fetch_apps/<string:tablename>", methods=['GET'])
def fetchdata_apps(tablename):
    #tablename='accnt'
    df = pd.DataFrame(fetch_data(tablename))
    return flask.jsonify(json.loads(df.to_json(orient='records')))


class FetchApp(Resource):
    def __init__(self):
        pass

    def get(self):
        #directory = config.project_sql
        api_list = [fname.split('.')[0] for fname in os.listdir(config.project_sql) if os.path.isdir(fname) == False]
        return flask.jsonify(api_list)


class GetViz(Resource):
    def __init__(self):
        pass

    def get(self):

        #directory = config.project_sql
        sql_file_list = [fname for fname in os.listdir(config.project_sql) if os.path.isdir(fname) == False and fname.endswith('.sql')]
        viz_file = generate_charts(sql_file_list)
        #print(viz_file)
        if '.' in viz_file:
            if viz_file.split('.')[1] == 'pdf' or viz_file.split('.')[1] == 'zip':
                return flask.send_file(viz_file)
            else:
                return viz_file
        else:
            return viz_file



class CustomSql(Resource):
    def __init__(self):
        pass

    # def get(self, custsql):
    #    return custsql

    def post(self):
        data = request.get_json()
        custom_data = fetch_data_custom(data)
        return json.loads(custom_data)


api.add_resource(FetchApp, '/fetch_apps')
api.add_resource(CustomSql, '/customsql')
api.add_resource(GetViz, '/getviz')
if __name__ == '__main__':
    app.run(debug=True)
