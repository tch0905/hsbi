from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def extract_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'grdPaging'})
    links = table.find_all('a')

    result = []
    for link in links:
        href = link.get('href')
        result.append(urljoin(url, href))

    return result

url = "https://di.hkex.com.hk/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/07/2023&sced=31/12/2023&sc=1477&src=MAIN&lang=EN&g_lang=en"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# find the table
table = soup.find('table', {'id': 'grdPaging'})

# find the link in the "Report Type" column
link = table.find('a', string='Complete list of substantial shareholders')

# extract the href attribute
href = link.get('href')

print(extract_link(url))