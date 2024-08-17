from csv import DictReader
import json
import pandas as pd


def ingest_csv_data(file_path: str):
    mydata: list = []
    with open(file_path, "r") as csvfile:
        reader: DictReader = DictReader(csvfile)
        for row in reader:
            mydata.append(row)
    return mydata


def ingest_json_data(file_path: str):
    with open(file_path, "r", encoding="utf-8-sig") as myfile:
        mydata = json.load(myfile)
    return mydata
