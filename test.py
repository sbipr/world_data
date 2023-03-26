import psycopg2
import sys
import boto3
import os
from dotenv.main import load_dotenv
from pprint import pprint

load_dotenv()

rds = boto3.client('rds',region_name='eu-west-2')

ENDPOINT="database-1.cok8qfd47nby.eu-west-2.rds.amazonaws.com"
PORT="5432"
USER="postgres"
REGION="eu-west-2"
DBNAME="postgres"
PASSWORD= os.environ['TOKEN']

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD, sslrootcert="SSLCERTIFICATE")
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    pprint(query_results)
except Exception as e:
    pprint("Database connection failed due to {}".format(e))                