import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json

user = "adriansdls"
pw = "0561784239Aa!"
host = "adriansdls.mysql.pythonanywhere-services.com"
database = "adriansdls$newspapers"

db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, pw, host, database), \
    connect_args = {'connect_timeout': 10})
conn = db.connect()

tables = conn.execute("SHOW TABLES;")

tables_lst = [table[0] for table in tables.fetchall()]

conn.close()

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/adriansdls/newspapers-366612-be359318d4f2.json", scope)
client = gspread.authorize(credentials)

today_news_sheet = client.open("today_news").sheet1
today_news = pd.DataFrame(today_news_sheet.get_all_records())

#url = 'https://drive.google.com/file/d/1PtNo_cOjgF-HXsmXEuBvV22ArM551mDH/view?usp=sharing'
#path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]
#today_news = pd.read_csv(path, sep=";")

today_news.to_sql('today_news', db)
today_news.head(1)