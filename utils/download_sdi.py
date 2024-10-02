from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
import os

def extract_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'grdPaging'})
    links = table.find_all('a')

    results = []
    for link in links:
        href = link.get('href')
        results.append((link.contents[0],urljoin(url, href)))

    return results

def extract_csv(content, url, path):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'grdPaging'})

    # Extract column names from table header
    headers = [th.text.strip() for th in table.find('tr', class_='boldtxtw').find_all('th')]
    headers = [th.text.strip() for th in table.find('tr', class_='boldtxtw').find_all('td')] if len(headers) == 0 else headers

    data = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        data.append([col.text.strip() for col in cols])

    df = pd.DataFrame(data, columns=headers)
    file_path = os.path.join(path, f'{content}.csv')
    df.to_csv(file_path, index=False)

