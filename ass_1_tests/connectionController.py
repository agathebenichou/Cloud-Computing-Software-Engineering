import requests
import json

URL = "http://127.0.0.1:5001"


def http_get(resource: str):
    response = requests.get(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response


def http_delete(resource: str):
    response = requests.delete(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response


def http_post(resource: str, data: {}):
    response = requests.post(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response


def http_put(resource: str, data: {}):
    response = requests.put(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response


def post_raw(resource: str, data:{}, headers: {}):
    response = requests.post(url=f"{URL}/{resource}", headers=headers, data=json.dumps(data))
    return response
