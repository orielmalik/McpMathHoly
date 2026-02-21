import os
import requests
from dotenv import load_dotenv

from Utils import consts
from Patterns.Singelton import LoggerSingelton

from functools import wraps


def find_and_load_env(filename=consts.filename, key_name=consts.key_name):
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            filepath = os.path.join(root, filename)
            load_dotenv(filepath)
            api_key = os.getenv(key_name)
            if api_key:
                return api_key.strip()
            else:
                return None
    return None


def call_apifreellm(api_key, builder):
    response = requests.post(
        consts.apf_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json=builder
    )
    return response.status_code, response.json()
