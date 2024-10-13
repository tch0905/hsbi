import os

import ollama
import chromadb
from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from utils.list_dir_in_dir import list_directories_in_directory
from utils.markdown_to_string import markdown_file_to_string
from utils.list_file_in_dir import list_files_in_directory
from utils.csv_to_markdown import csv_to_markdown
from utils.markdown_to_string import markdown_file_to_string

import json

def extract_first_json_dict(json_string):
    # Find the first JSON object in the string
    start_index = json_string.find('{')
    end_index = json_string.find('}') + 1
    first_json_obj = json_string[start_index:end_index]

    # Parse the first JSON object into a dictionary
    print(first_json_obj)
    data = json.loads(first_json_obj)
    return data


return_data = []
non_free_float_list = []
path = 'src'
ric_list = list_directories_in_directory(path)
print(ric_list)
# ollama need to be created befoer runing
prompt_4_embedding_search = ''''II. Movements in Issued Shares, Balance at close of preceding month
'''
response = ollama.embeddings(
    prompt=prompt_4_embedding_search,
    model="mxbai-embed-large"
)
print(response)
for ric in ric_list:
    # if ric in ['0002','0011','0038','0069','0136','0151']:
    #     continue
    non_free_float_list = []
    return_data = []
    print(ric,':')
    prompt = (f"What is the Number of issued shares (excluding treasury shares)of {ric}, balance at close of the month?, which shouldn\'t is not with the authorized/registered shares. You should find in II. Movements in Issued Shares,"
              f" ")

    vector_directory = f'./temp/{ric}'
    client = chromadb.PersistentClient(path=vector_directory)
    collection = client.get_collection(name=f"ric{ric}")
    # generate an embedding for the prompt and retrieve the most relevant doc

    # n_results is the number of page that the vector db take out
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=8
    )
    data = results['documents'][0]
    print(data)


    output = ollama.generate(
        model="hsbi",
        prompt=f"Please return a json format only, if u can't output, return -1. Using this data: {data}. Respond to this prompt: {prompt}"
    )

    print(output['response'])
    total_share = 0
    try:
        total_share = extract_first_json_dict(output['response'])
    except:
        total_share = 0

    import csv
    path = f'./src/{ric}/Consolidated list of substantial shareholders.csv'
    # Sample CSV data
    # Read the CSV file and extract desired columns
    members = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            shareholder_name = row['Name of substantial shareholder']
            shares_interested = row['Number of shares interested (See *Notes above)']
            print(f'{shareholder_name}, {shares_interested}')
            members.append([shareholder_name, shares_interested])

    for member in members:


        prompt = f'Is the member,{member[0]} , is custodians, trustees, mutual funds and investment companies?'
        search_prompt = f'{member[0]}, {member[1]}'
        response = ollama.embeddings(
            prompt=search_prompt,
            model="mxbai-embed-large"
        )
        results = collection.query(
            query_embeddings=[response["embedding"]],
            n_results=3
        )
        data = results['documents'][0]
        output = ollama.generate(
            model="hsbi",
            prompt=f"Please return a json format only. Data: {data}.  Respond to this prompt: {prompt}"
        )
        count_free_flaot = output['response']
        print(output['response'])


        prompt = f'Is the member,{member[0]},  shares belong free-float? We need find the member us related what first.'
        search_prompt = f'{member[0]}'
        response = ollama.embeddings(
            prompt=search_prompt,
            model="mxbai-embed-large"
        )
        results = collection.query(
            query_embeddings=[response["embedding"]],
            n_results=3
        )
        data = results['documents'][0]
        output = ollama.generate(
            model="hsbi",
            prompt=f"Please return a json format only. Data: {data}. Respond to this prompt: {prompt}"
        )
        print("question 2:")
        print(output['response'])


        prompt = f'Is the member,{member[0]},  shares belong free-float?Where it share equal {member[1]} We need find the member us related what first.'
        note = f'Shares held by any entities (excluding custodians, trustees, mutual funds and investment companies) which control more than 5% of the shareholdings would be considered as non-freefloat and are excluded from index calculation:'
        search_prompt = f"{member[0]}, {output['response']}"
        response = ollama.embeddings(
            prompt=search_prompt,
            model="mxbai-embed-large"
        )

        results = collection.query(
            query_embeddings=[response["embedding"]],
            n_results=5
        )

        data = results['documents'][0]
        output = ollama.generate(
            model="hsbi",
            prompt=f"Please return a json format only. Note: {note}. Data: {data} Respond to this prompt: {prompt}, "
                   f"Note that their share may be update, please return the update share"
                   f"record: {output['response']}, total share: {total_share}, other info: {count_free_flaot} If the "
                   f"share of the member / total shares > 5%, the member not custodians, trustees, mutual funds and "
                   f"investment companies. Then should be non-freefloat."
                   f"If the member is custodians, trustees, mutual funds and investment companies. No matter "
                   f"he/she/it have over 5%, condiser it is free-float"
        )
        print(output['response'])

        try:
            is_ff = extract_first_json_dict(output['response'])["freefloat"]
            print(is_ff)
            if is_ff == False or is_ff == 'false' or is_ff == 'False':
                non_free_float_list.append(member[0])
        except:
            is_ff = False
            non_free_float_list.append(member[0])
        try:
            if extract_first_json_dict(output['response'])["share_of_member"] == 0:
                return_data.append([member, member[1], is_ff])
            else:
                return_data.append([member, extract_first_json_dict(output['response'])["share_of_member"], is_ff])
        except:
            return_data.append([member, member[1], is_ff])

    import csv



    # CSV file name
    csv_file = f"./result/{ric}/shares_data.csv"
    os.makedirs(f"./result/{ric}/", exist_ok=True)

    # Writing data to the CSV file
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["member", "shares", "free float"])  # Write header

            for row in return_data:
                writer.writerow(row)
    except:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["member", "shares", "free float"])  # Write header


    print(f"Data has been written to {csv_file}.")

