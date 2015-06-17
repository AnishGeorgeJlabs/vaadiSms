# -*- encoding: utf-8 -*-

# This module does the data downloading part from the csv
import csv
import requests
import datetime
import zipfile
from bs4 import BeautifulSoup
from config import config

# ------------ Helper functions ------------------
def str_to_hex(text):
    text = text.strip("u").strip("'")
    arabic_hex = [hex(ord(b)).replace("x","").upper().zfill(4) for b in text]
    arabic_hex.append("000A")
    text_update = "".join(arabic_hex)
    return text_update
# ------------------------------------------------



# --------------------- Main method ------------------------
def load_data():
    try:
        DATAURL = config['data_url']
        r = requests.get(DATAURL)
        datafile = "data" + str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".csv"
        if r.status_code is 200:    # Todo: change this
            f = open(datafile,"w")
            kl = r.text
            f.write(r.text)
            f.close()
        CONTENTURL = config['content_url']
        contentfile = "con" + str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".zip"
        r = requests.get(CONTENTURL)
        if r.status_code is 200:
            f = open(contentfile,"wb")
            f.write(r.content)
            f.close()
        zf = zipfile.ZipFile(contentfile)
        data = zf.read("Sheet1.html")
        soup = BeautifulSoup(data,"html5lib")
        td = soup.findAll("td")
        en = td[2].text.strip()
        ar = td[3].text.strip()
        sms_dict = {'ar':ar,'en':en}
        data = []
        cc = csv.reader(kl.split("\n"))
        for x in cc:
            data.append(x)

        payloadArr = []
        for d in data:
            payload = {}
            if d[1].strip() in "Arabic":
                message_text = sms_dict['ar']
                payload = {'message': str_to_hex(message_text),'mobilenumber':d[0].strip("=").strip(), 'mtype': "OL"}
            elif d[1].strip() in "English":
                message_text = sms_dict['en']
                payload = {'message': str_to_hex(message_text),'mobilenumber':d[0].strip("=").strip(), 'mtype': "N"}
            payloadArr.append(payload)

        return (True, payloadArr)
    except Exception:
        return (False, None, None)
    finally:
        pass
# -----------------------------------------------------------
