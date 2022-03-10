import psycopg2
from config import config

# Connect ot DB and fetch result set by executing query on DB
def execute_sql(query):
    try:
        conn = psycopg2.connect(**config.config)
    except psycopg2.OperationalError as e:
        print(f'Unable to connect!\n{e}')
        conn = None
    if conn is not None:
        cur = conn.cursor()
        try:
            cur.execute(query)
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return cols, rows
        except Exception as e:
            print(e)
            return "SQLError"
        finally:
            cur.close()
            conn.close()
    else:
        return "ConnError"


def fetch_resulset(query):
    failed_flag = 'failed'
    if execute_sql(query) == 'SQLError':
        return failed_flag, "Could not fetch Results. Failed to execute SQL. Check SQL statement"
    if execute_sql(query) == 'ConnError':
        return failed_flag, "Failed to connect to Database. Check connection details."
    return execute_sql(query)

