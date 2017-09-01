import requests
import json

REPO_RELEASE = "https://api.github.com/repos/ojdkbuild/ojdkbuild/releases"

def getReleaseAssets(tag):
    req = requests.get(REPO_RELEASE)
    for item in req.json():
        if item["tag_name"] == tag:
            return item["assets"]
    
    raise RuntimeError("No tag of {} found".format(tag))


def getBinaryOfWindows(assets):
    FILTER_LIST = [
        lambda x: x["name"].find("windows") != -1,
        lambda x: x["name"].find("debuginfo") == -1,
        lambda x: x["name"].find("src") == -1,
        lambda x: x["name"].find("debug") == -1,
        lambda x: x["name"].endswith(".zip")
    ]
    for item in FILTER_LIST:
        assets = filter(item, assets)

    return map(lambda x: {
        "url": x["browser_download_url"],
        "name": x["name"]
    }, assets)
