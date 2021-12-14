from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import tempfile
import os
from google.cloud import storage

storage_client = storage.Client()

def scrape_data():
    url = 'https://store.steampowered.com/stats/'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    data_dict = {}

    stats_detail = soup.find(id='detailStats')
    for i, val in enumerate(stats_detail.find_all('tr')):
        if i < 2:
            continue

        tr_list = val.find_all('td')
        key_data = clean_data(tr_list[3].get_text())
        val_data = clean_data(tr_list[1].get_text())
        data_dict[key_data] = int(val_data)

    return data_dict

def clean_data(text):
    text = text.replace('\n', '')
    text = text.replace(',', '')
    
    return text

def make_df(data_dict):
    df = pd.DataFrame.from_dict(data_dict, orient='index').T
    today = datetime.date.today()
    df = df.rename(index={0: today})

    return df

def upload_gcs(df):
    _, temp_local_filename = tempfile.mkstemp()
    df.to_csv(temp_local_filename, index_label='date')

    today = datetime.date.today()
    today_str = today.strftime('%Y_%m_%d')
    
    bucket = storage_client.bucket('YOUR_BUCKET_NAME')
    blob = bucket.blob(today_str + '_steam_max.csv')
    blob.upload_from_filename(temp_local_filename)
    
    os.remove(temp_local_filename)
    
    return 'Uploaded!'

def main(event, context):
    upload_gcs(make_df(scrape_data()))