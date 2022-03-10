from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_FILE=os.path.join(BASE_DIR, 'root.crt')

project_home = BASE_DIR
project_temp = os.path.join(BASE_DIR, 'temp')
project_sql = os.path.join(BASE_DIR, 'sql')

NAME = os.environ.get('JDV_SCHEMA')
USER = os.environ.get('JDV_USER')
PASSWORD = os.environ.get('JDV_PASSWORD')
HOST = os.environ.get('JDV_HOST') if os.environ.get('JDV_HOST') is not None else 'jdv.prod.a4.vary.redhat.com'
PORT = os.environ.get('JDV_PORT') if os.environ.get('JDV_PORT') is not None else 35432
config = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'password': PASSWORD,
        'database': NAME,
        'sslmode': 'verify-ca',
        'sslrootcert': ROOT_FILE
    }
