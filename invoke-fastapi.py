import requests, sys
import json


# url = "http://localhost:5000/items"  # Replace with the actual URL of your FastAPI server
url = "http://34.41.189.117:5000/items" 
data = {"name": "Example Item", "description": "This is an example item."}

response = requests.post(url, json=data)

print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())