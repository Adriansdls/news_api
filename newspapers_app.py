
from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
from datetime import date
from unidecode import unidecode
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql
from sqlalchemy import create_engine
import json

user = "adriansdls"
pw = "0561784239Aa!"
host = "adriansdls.mysql.pythonanywhere-services.com"
database = "adriansdls$newspapers"

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

app = Flask(__name__)

def connect():
    db = create_engine(
        'mysql+pymysql://{0}:{1}@{2}/{3}' \
            .format(user, pw, host, database), \
        connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnet(conn):
    conn.close()

@app.route('/', methods=['GET'])
def home():
    return "try /eldiario/<string:num>"

#@app.route('/eldiario/<string:num>', methods=['GET'])
#def by_num(num):
 #   num = int(num)
  #  df = pd.read_csv("/Users/adriansanchezdelasierra/projects/news_parser/new_crawler/csvs/el_diario_full.csv")
   # return df.iloc[num].text

credentials = ServiceAccountCredentials.from_json_keyfile_name("/home/adriansdls/newspapers-366612-be359318d4f2.json", scope)
client = gspread.authorize(credentials)

@app.route('/eldiario/url/<string:url>', methods=['GET'])
def by_url(url):
    df = pd.read_csv("/Users/adriansanchezdelasierra/projects/news_parser/new_crawler/csvs/el_diario_full.csv")
    url = "https://www.eldiario.es/{0}".format(url)
    iloc_ = df.url[df["url"] == url].index
    return str(df.text.iloc[iloc_])

@app.route('/eldiario', methods=['GET'])
def get_all_diario():
    today = date.today().isoformat()
    df = pd.read_csv("/Users/adriansanchezdelasierra/projects/news_parser/new_crawler/csvs/el_diario_full.csv")
    df_today = df[df.date == today]
    df_today = df_today[["title","text"]]

    result = {}
    for index, row in df_today.iterrows():
        #result[index] = dict(row)
        #result[row["title"]] = row["text"]
        result[index] = unidecode(row["title"])
    return result

@app.route('/eldiario/<string:num>', methods=['GET'])
def by_id(num):
    num= int(num)
    today = date.today().isoformat()
    df = pd.read_csv("/Users/adriansanchezdelasierra/projects/news_parser/new_crawler/csvs/el_diario_full.csv")
    df_today = df[df.date == today]
    df_today = df_today[["title","text"]]
    return unidecode(df_today.text.loc[num])

@app.route('/ser', methods=['GET'])
def get_all_ser():
    today = date.today().isoformat()
    df = pd.read_csv("/Users/adriansanchezdelasierra/projects/news_parser/new_crawler/csvs/cadena_ser_full.csv")
    df_today = df[df.fecha == today]
    df_today = df_today[["titulo","texto"]]

    result = {}
    for index, row in df_today.iterrows():
        #result[index] = dict(row)
        #result[row["title"]] = row["text"]
        result[index] = unidecode(row["titulo"])
    return result

@app.route('/ser/<string:num>', methods=['GET'])
def by_id_ser(num):
    num= int(num)
    today = date.today().isoformat()
    df = pd.read_csv("/Users/adriansanchezdelasierra/projects/news_parser/new_crawler/csvs/cadena_ser_full.csv")
    df_today = df[df.fecha == today]
    df_today = df_today[["titulo","texto"]]
    return unidecode(df_today.texto.loc[num])

@app.route('/today', methods=['GET'])
def today():
    today_sheet = client.open("today_news").sheet1
    today = pd.DataFrame(today_sheet.get_all_records())
    return unidecode(df_today)

app.run()