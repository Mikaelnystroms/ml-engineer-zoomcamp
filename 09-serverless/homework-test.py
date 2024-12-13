import requests
import json

url = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"

# Add timeout to prevent hanging
response = requests.post(
    "http://localhost:8080/2015-03-31/functions/function/invocations",
    json={"url": url},
    timeout=10  # Add timeout
)

# Add error handling
if response.status_code == 200:
    result = response.json()
    print(f"Prediction: {result}")
else:
    print(f"Error: Status code {response.status_code}")
    print(f"Response: {response.text}")