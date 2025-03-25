import json


def load_data() -> dict:
    with open("stocks.json", 'r') as f:
        data = json.load(f)
        return data

