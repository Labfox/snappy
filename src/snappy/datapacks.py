import requests

def get_datapack(dt_id):
    return requests.get(f"https://raw.githubusercontent.com/Labfox/snappy/refs/heads/main/datapacks/{dt_id}.json").text

def get_index(index_id):
    return requests.get(f"https://raw.githubusercontent.com/Labfox/snappy/refs/heads/main/datapacks/by/{index_id}.json").text