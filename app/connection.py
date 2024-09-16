from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()    # load environment variables from .env file

# Get the connection parameters from environment variables
host = os.environ['PG_HOST']
port = os.environ['PG_PORT']
username = os.environ['PG_USERNAME']
password = os.environ['PG_PASSWORD']
database = os.environ['PG_DATABASE']

# Establish a connection
conn = psycopg2.connect(
    host=host,
    port=port,
    user=username,
    password=password,
    dbname=database
)

# Create a cursor object


