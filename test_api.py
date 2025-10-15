import requests

url = "http://127.0.0.1:5000/predict"
data = {"text": "This is a fake news article."}
response = requests.post(url, json=data)

print("Prediction:", response.json())