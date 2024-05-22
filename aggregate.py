import json
import random
import datetime
from pymongo import MongoClient
from collections import defaultdict


from config import MONGO_URI 

client = MongoClient(MONGO_URI)
db = client['salaries']
collection = db['salary']



def write_data_to_mongo():
    collection.delete_many({})

    dt_from = datetime.datetime(2022, 1, 1, 0, 0, 0)
    dt_upto = datetime.datetime(2022, 12, 31, 23, 59, 0)

    while dt_from <= dt_upto:
        document = {
            "timestamp": dt_from.isoformat(), "value": random.randint(1000, 10000)
        }

        collection.insert_one(document)
        dt_from += datetime.timedelta(hours=1)


def read_data_from_mongo():

    documents = collection.find()

    hours = []
    data = []

    for doc in documents:
        data.append(doc["value"])
        hours.append(doc["timestamp"])
    return hours, data




def aggregating_data(start, end, group_type):
    print("Getting Data")
    global key
    dt_from = datetime.datetime.fromisoformat(start)
    dt_upto = datetime.datetime.fromisoformat(end)

    hourly_labels, hourly_dataset = read_data_from_mongo()
    grouped_data = defaultdict(int)

    for i, label in enumerate(hourly_labels):
        current_date = datetime.datetime.fromisoformat(label)
        if dt_from <= current_date <= dt_upto:
            if group_type not in ["month", 'hour', "day"]:
                return
            elif group_type == 'hour':
                key = label
            elif group_type == 'day':
                key = current_date.date().isoformat() + "T00:00:00"
            elif group_type == 'month':
                key = current_date.strftime('%Y-%m-01T00:00:00')
            grouped_data[key] += hourly_dataset[i]

    sorted_keys = sorted(grouped_data.keys())
    grouped_sums = [grouped_data[key] for key in sorted_keys]

    return {
        "dataset": grouped_sums, "labels": sorted_keys
    }


#dataset_input = input('Enter a dataset in format {"dt_from": "2022-01-01T00:00:00",  "dt_upto": "2022-01-01T02:00:00", "group_type": "day"}: ')
#data_dict = json.loads(dataset_input.replace("'", "\""))
#print(aggregating_data(data_dict['dt_from'], data_dict["dt_upto"], data_dict["group_type"]))

