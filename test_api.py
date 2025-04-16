import requests
import json

API_KEY = 'b26fd0bbc06eab2f82011565d292c129'
url = 'https://api.elsevier.com/content/search/scopus'
params = {
    'query': 'AFFILCOUNTRY("Russian Federation") AND PUBYEAR > 2013',
    'count': 1
}
headers = {
    'X-ELS-APIKey': API_KEY
}

response = requests.get(url, headers=headers, params=params)
print("Status:", response.status_code)
print("URL:", response.url)
print(response.json())


def save_as_json(data):
    with open("data_json.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


save_as_json(response.json())