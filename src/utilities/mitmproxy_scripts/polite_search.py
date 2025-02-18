import getpass
import json

username = getpass.getuser()


def insert(record):
    with open(
        rf"C:\Users\{username}\Documents\polite_search.json", "w", encoding="utf-8"
    ) as f:
        json.dump(record, f)


def response(flow):
    data = {}
    if "cuacua.coccoc.com" in flow.request.url:
        data["url"] = flow.request.url
        for item in flow.request.headers:
            data[item] = flow.request.headers[item]
        insert(data)
