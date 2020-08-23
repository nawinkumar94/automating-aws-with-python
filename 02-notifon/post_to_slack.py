# coding: utf-8
import requests
url =  # Add the slack url
data = {"text":"Hello, World!"}
requests.post(url,json=data)
