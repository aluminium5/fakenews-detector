import requests

response = requests.post(
    "http://127.0.0.1:5000/predict",
    json={"text": "This is a news headline!"}
)

print("Response:", response.json())