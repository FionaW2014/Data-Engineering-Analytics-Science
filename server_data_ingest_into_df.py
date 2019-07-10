# -*- coding: utf-8 -*-
"""
Created on May 30 2019

@author: Fiona Wang
"""
import psycopg2  #terminal: pip install psycopg2
import pandas as pd  #after downloading pandas or work in environment with pandas
import pandas.io.sql as psql
import sys
def table_to_csv(sql, file_path, dbname, host, port, user, pwd):
    '''
    This function creates a csv file from PostgreSQL with query
    '''
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port,\
         user=user, password=pwd)
        print("Connecting to Database")
        # Get data into pandas dataframe
        df = pd.read_sql(sql, conn)
        # Write to csv file
        df.to_csv(file_path, encoding='utf-8', header = True,\
         doublequote = True, sep=',', index=False)
        print("CSV File has been created")
        conn.close()

    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(1)

# Execution Example with transaction table
sql = 'select * from schema_name.table_name order by column1, column2'  #write in your SQL code, with quotation marks
file_path = 'give your path where you want to store/created_table.csv'
dbname = 'xxxxxx'
host = 'x.xxx.xxx.xxx'  #IP address
port = '5432'  #typically is 5432
user = 'xxxxxxx'
pwd = 'xxxxx'

table_to_csv(sql, file_path, dbname, host, port, user, pwd)