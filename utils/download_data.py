import download_sdi
import csv
import os
import requests
import re

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded and saved as {filename}")
    else:
        print(f"Failed to download PDF from {url}")

def main(input_path, output_dir):
    with open(input_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for header, url in row.items():
                pattern = r'(\d*)\.HK'
                match = re.findall(pattern, url)
                if match:
                    ric_path = os.path.join(output_dir, match[0])
                    os.makedirs(ric_path, exist_ok=True)
                if header == 'SDI':
                    result = download_sdi.extract_link(url)
                    for content, link in result:
                        download_sdi.extract_csv(content, link,ric_path)
                if header == "Financial report":
                    urls = url.split("\n")
                    for url in urls:
                        filename = os.path.basename(url)
                        file_path = os.path.join(ric_path, filename)
                        download_pdf(url, file_path)


if __name__ == "__main__":
    path = '../data_explorer/faf_documents.csv'
    output = '../src'
    main(path,output)