import json
from bs4 import BeautifulSoup
import sys
import os
import urllib.request
import tarfile
import zipfile
import pandas as pd
import numpy as np
import pickle

def isDate(text):
    if len(text) > 20:
        return False
    dates = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    # dates = ["1,", "2,", "3,", "4,", "5,", "6,", "7,", "8,", "9,", "0,"]
    flag_date = False
    for date in dates:
        if date in text:
            flag_date = True
    return flag_date

def get_judge_date(file_name):
    with open(file_name, 'rb') as jf:
        entry = json.load(jf)
        ht = BeautifulSoup(entry["html_lawbox"], "html.parser")
        i = 0; judge = ""; date = ""; j = 0
        while not "Judge" in judge:
            judge = ht.find_all("p")[i].get_text()
            i += 1
        #print(ht.find_all("center"))
        while not isDate(date):
            try:
                date = ht.find_all("center")[j].get_text()
            except:
                date = ""
                break
            j += 1
    return judge, date

def maybe_download_and_extract(url, download_dir):
    filename = url.split('/')[-1]
    file_path = os.path.join(download_dir, filename)

    # Check if the file already exists.
    # If it exists then we assume it has also been extracted,
    # otherwise we need to download and extract it now.
    if not os.path.exists(file_path):
        # Check if the download directory exists, otherwise create it.
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Download the file from the internet.
        file_path, _ = urllib.request.urlretrieve(url=url,
                                                  filename=file_path
                                                  )
        print("Download finished. Extracting files.")
        if file_path.endswith(".zip"):
            # Unpack the zip-file.
            zipfile.ZipFile(file=file_path, mode="r").extractall(download_dir)
        elif file_path.endswith((".tar.gz", ".tgz")):
            # Unpack the tar-ball.
            tarfile.open(name=file_path, mode="r:gz").extractall(download_dir)
        print("Done.")
    else:
        print("Data has apparently already been downloaded and unpacked.")

def save_summary(file_path, district):
    judges = []; file_names = []; dates = []
    for file_name in os.listdir(file_path):
        if file_name.endswith(".json"):
            judge, date = get_judge_date(file_path + file_name)
            file_names += [file_name]
            judges += [judge.split(",")[0]]
            dates += [date[:-1]]
    data = {"judges": judges, "dates": dates, "file_names": file_names}
    df = pd.DataFrame(data, columns=["judges", "dates", "file_names"])
    if not os.path.exists("summary_tables"):
        os.makedirs("summary_tables")
    pickle.dump(df, open("summary_tables/"+district + "_summary.p", "wb"))

def load_summary(district):
    return pickle.load(open("summary_tables/"+district + "_summary.p", "rb"))

def main():
    districts = {"Louisiana":["laeb", "lamb", "lawb"], "Missouri": ["moeb", "mowb"], "NewYork": ["nyeb", "nynb", "nysb", "nywb"]}
    for district in districts["Louisiana"]:
        file_path = "opinions/" + district + "/"
        maybe_download_and_extract("https://www.courtlistener.com/api/bulk-data/opinions/"+district+".tar.gz", file_path)
        save_summary(file_path, district)

   for district in districts["Missouri"]:
       file_path = "opinions/" + district + "/"
       maybe_download_and_extract("https://www.courtlistener.com/api/bulk-data/opinions/"+district+".tar.gz", file_path)
       save_summary(file_path, district)
   print("Finished Missouri")

    for district in districts["NewYork"]:
        file_path = "opinions/" + district + "/"
        maybe_download_and_extract("https://www.courtlistener.com/api/bulk-data/opinions/"+district+".tar.gz", file_path)
        save_summary(file_path, district)
if __name__ == "__main__":
    main()

Hello, I am just trying the merging func in git
wow
