import os
import json

data_file_path = os.path.join(os.path.dirname(__file__), '../data/db.json')
guest_file_path = os.path.join(os.path.dirname(__file__), '../data/user.json')

def init_data_file():
    if not os.path.exists(data_file_path):
        with open(data_file_path, 'w') as f:
            json.dump({"users": []}, f, indent=2)
    
    if not os.path.exists(guest_file_path):
        with open(guest_file_path, 'w') as f:
            json.dump({"guest": {}}, f, indent=2)

def read_data():
    try:
        with open(data_file_path, 'r') as f:
            return json.load(f)
    except Exception as err:
        print(f"Error reading data file: {err}")
        return {}

def write_data(data):
    try:
        with open(data_file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as err:
        print(f"Error writing data file: {err}")

def read_guest_data():
    try:
        with open(guest_file_path, 'r') as f:
            return json.load(f)
    except Exception as err:
        print(f"Error reading guest data file: {err}")
        return {}

def write_guest_data(data):
    try:
        with open(guest_file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as err:
        print(f"Error writing guest data file: {err}")
