import requests

url = "https://ha14najcu4.execute-api.eu-north-1.amazonaws.com/test/predict"

data = {"url": "http://bit.ly/mlbookcamp-pants"}

response = requests.post(url, json=data)
print(response.text)  # Print the raw response
print(response.status_code)  # Print the status code
