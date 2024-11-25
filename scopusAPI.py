import requests
import time
import pandas as pd
from query import base_query, start_index, count_index
from common_data import BASE_API_KEY

API_KEY = BASE_API_KEY
SEARCH_URL = 'https://api.elsevier.com/content/search/scopus'
ABSTRACT_URL = 'https://api.elsevier.com/content/abstract/eid/'
HEADERS = {'X-ELS-APIKey': API_KEY}

query = base_query
start = start_index
count = count_index
results = []

while True:
    params = {
        'query': query,
        'start': start,
        'count': count
    }
    response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    data = response.json()

    if 'search-results' not in data:
        break

    entries = data['search-results']['entry']
    results.extend(entries)

    if len(entries) < count:
        break

    start += count
    time.sleep(1)

# Получение Abstract и References
detailed_results = []
for entry in results:
    eid = entry.get('eid', '')
    if not eid:
        continue

    # Запрос к Abstract Retrieval API
    abstract_response = requests.get(f"{ABSTRACT_URL}{eid}", headers=HEADERS)
    if abstract_response.status_code != 200:
        print(f"Не удалось получить данные для EID {eid}")
        continue

    abstract_data = abstract_response.json()
    abstract = abstract_data.get('abstracts-retrieval-response', {}).get('coredata', {}).get('dc:description', '')
    references = abstract_data.get('abstracts-retrieval-response', {}).get('item', {}).get('bibrecord', {}).get('tail',
                                                                                                                {}).get(
        'bibliography', {}).get('reference', [])

    # Обработка данных
    reference_list = []
    if references:
        for ref in references:
            ref_text = ref.get('ref-info', {}).get('ref-title', {}).get('ref-titletext', '')
            reference_list.append(ref_text)

    detailed_results.append({
        'Title': entry.get('dc:title', ''),
        'Publication Name': entry.get('prism:publicationName', ''),
        'Publication Year': entry.get('prism:coverDate', '').split('-')[0],
        'DOI': entry.get('prism:doi', ''),
        'Authors': entry.get('dc:creator', ''),
        'Affiliation': entry.get('affiliation', [{}])[0].get('affilname', ''),
        'Abstract': abstract,
        'References': '; '.join(reference_list)
    })
    time.sleep(1)

# Сохранение в Excel
df = pd.DataFrame(detailed_results)
output_file = 'scopus_data_russia_with_abstracts.xlsx'
df.to_excel(output_file, index=False)

print(f'Данные с Abstract и References сохранены в файл {output_file}')