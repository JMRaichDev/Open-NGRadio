import requests


def getRadioApiJSON():
    return requests.get(
        "http://apiv2.nationsglory.fr/radio/api.json").json()  # parsing api.json and returning content as JSON
