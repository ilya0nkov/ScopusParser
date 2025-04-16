import requests
import time
import pandas as pd

API_KEY = 'b26fd0bbc06eab2f82011565d292c129'
BASE_URL = 'https://api.elsevier.com/content/search/scopus'
HEADERS = {'X-ELS-APIKey': API_KEY}

query = 'AFFILCOUNTRY(Russia) AND PUBYEAR > 2013'
start = 0
count = 25
results = []

while True:
    params = {
        'query': query,
        'start': start,
        'count': count
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    data = response.json()

    if 'search-results' not in data:
        break

    entries = data['search-results']['entry']
    results.extend(entries)

    if len(entries) < count:
        break

    start += count
    time.sleep(1)  # Уважайте лимиты API

# Преобразуем данные в DataFrame
df = pd.DataFrame(results)

# Сохраняем в Excel
output_file = 'scopus_data_russia.xlsx'
df.to_excel(output_file, index=False)

print(f'Данные сохранены в файл {output_file}')
