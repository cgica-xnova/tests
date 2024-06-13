import requests
import boto3
import json
import sys
import os
import re
import streamlit as st
import pandas as pd
import numpy as np
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed

all_countries =[
        "DNK",
        "IRL",
        "SWE",
        "FIN",
        "NOR",
        "ISL",
        "FRO",
        "EST",
        "LVA",
        "LTU",
        "POL",
        "UKR",
        "MKD",
        "MDA",
        "SVN",
        "BGR",
        "CZE",
        "ROU",
        "SRB",
        "ALB",
        "BIH",
        "SVK",
        "HRV",
        "RUS",
        "FRA",
        "DEU",
        "GBR",
        "NLD",
        "BEL",
        "AUT",
        "HUN",
        "LUX",
        "MCO",
        "CHE",
        "ESP",
        "ITA",
        "TUR",
        "PRT",
        "GRC",
        "MLT",
        "CYP",
        "AND"
    ]

countries = {
 'All': 'ALL',
 'Spain': 'ESP',
 'Italy': 'ITA',
 'Netherlands': 'NLD',
 'Portugal': 'PRT',
 'France': 'FRA',
 'Belgium': 'BEL',
 'Greece': 'GRC',
 'Germany': 'DEU',
 'United Kingdom': 'GBR',
 'Albania': 'ALB',
 'Algeria': 'DZA',
 'Angola': 'AGO',
 'Antigua and Barbuda': 'ATG',
 'Argentina': 'ARG',
 'Aruba': 'ABW',
 'Australia': 'AUS',
 'Austria': 'AUT',
 'Azerbaijan': 'AZE',
 'Bahrain': 'BHR',
 'Bangladesh': 'BGD',
 'Barbados': 'BRB',
 'Belarus': 'BLR',
 'Belize': 'BLZ',
 'Benin': 'BEN',
 'Bermuda': 'BMU',
 'Plurinational State of Bolivia': 'BOL',
 'Bosnia and Herzegovina': 'BIH',
 'Botswana': 'BWA',
 'Brasil': 'BRA',
 'British Indian Ocean Territory': 'IOT',
 'British Virgin Islands': 'VGB',
 'Brunei Darussalam': 'BRN',
 'Bulgaria': 'BGR',
 'Burkina Faso': 'BFA',
 'Burundi': 'BDI',
 'Cabo Verde': 'CPV',
 'Cambodia': 'KHM',
 'Cameroon': 'CMR',
 'Canada': 'CAN',
 'Cayman Islands': 'CYM',
 'Central African Republic': 'CAF',
 'Chad': 'TCD',
 'Chile': 'CHL',
 'China': 'CHN',
 'Christmas Islands': 'CXR',
 'Cocos Islands': 'CCK',
 'Colombia': 'COL',
 'Comoros': 'COM',
 'Congo': 'COG',
 'Democratic Republic of Congo': 'COD',
 'Cook Islands': 'COK',
 'Costa Rica': 'CRI',
 "Côte d'Ivoire": 'CIV',
 'Croatia': 'HRV',
 'Cuba': 'CUB',
 'Curaçao': 'CUW',
 'Cyprus': 'CYP',
 'Czech Republic': 'CZE',
 'Denmark': 'DNK',
 'Djibouti': 'DJI',
 'Dominica': 'DMA',
 'Dominican Republic': 'DOM',
 'Ecuador': 'ECU',
 'Egypt': 'EGY',
 'El Salvador': 'SLV',
 'Equatorial Guinea': 'GNQ',
 'Eritrea': 'ERI',
 'Estonia': 'EST',
 'Eswatini': 'SWZ',
 'Ethiopia': 'ETH',
 'Faroe Islands': 'FRO',
 'Fiji': 'FJI',
 'Finland': 'FIN',
 'Falkland Islands(Malvinas)': 'FLK',
 'French Guiana': 'GUF',
 'French Polynesia': 'PYF',
 'French Southern and Antarctic Territories': 'ATF',
 'Gabon': 'GAB',
 'Gambia': 'GMB',
 'Georgia': 'GEO',
 'Ghana': 'GHA',
 'Gibraltar': 'GIB',
 'Greenland': 'GRL',
 'Grenada': 'GRD',
 'Guam': 'GUM',
 'Guatemala': 'GTM',
 'Guinea': 'GIN',
 'Guinea - Bissau': 'GNB',
 'Guyana': 'GUY',
 'Haiti': 'HTI',
 'Honduras': 'HND',
 'Hong Kong, China': 'HKG',
 'Hungary': 'HUN',
 'Iceland': 'ISL',
 'India': 'IND',
 'Indonesia': 'IDN',
 'Iran, Islamic Republic of': 'IRN',
 'Iraq': 'IRQ',
 'Ireland': 'IRL',
 'Israel': 'ISR',
 'Jamaica': 'JAM',
 'Japan': 'JPN',
 'Jordan': 'JOR',
 'Kazakhstan': 'KAZ',
 'Kenya': 'KEN',
 'Kiribati': 'KIR',
 "Democratic People's Republic of Korea": 'PRK',
 'Republic of Korea': 'KOR',
 'Kuwait': 'KWT',
 'Kyrgyzstan': 'KGZ',
 "Lao People's Democratic Republic": 'LAO',
 'Latvia': 'LVA',
 'Lebanon': 'LBN',
 'Lesotho': 'LSO',
 'Liberia': 'LBR',
 'State of Libya': 'LBY',
 'Lithuania': 'LTU',
 'Luxembourg': 'LUX',
 'Macao, China': 'MAC',
 'North Macedonia': 'MKD',
 'Madagascar': 'MDG',
 'Malawi': 'MWI',
 'Malaysia': 'MYS',
 'Maldives': 'MDV',
 'Mali': 'MLI',
 'Malta': 'MLT',
 'Marshall Islands': 'MHL',
 'Martinique': 'MTQ',
 'Mauritania': 'MRT',
 'Mauritius': 'MUS',
 'Mayotte': 'MYT',
 'Mexico': 'MEX',
 'Federated States of Micronesia': 'FSM',
 'Republic of Moldova': 'MDA',
 'Monaco': 'MCO',
 'Mongolia': 'MNG',
 'Montenegro': 'MNE',
 'Montserrat': 'MSR',
 'Morocco': 'MAR',
 'Mozambique': 'MOZ',
 'Myanmar': 'MMR',
 'Namibia': 'NAM',
 'Nauru': 'NRU',
 'Nepal': 'NPL',
 'New Caledonia': 'NCL',
 'New Zealand': 'NZL',
 'Nicaragua': 'NIC',
 'Niger': 'NER',
 'Nigeria': 'NGA',
 'Niue': 'NIU',
 'Norfolk Island': 'NFK',
 'Norway': 'NOR',
 'Oman': 'OMN',
 'Pakistan': 'PAK',
 'Palau': 'PLW',
 'State of Palestine': 'PSE',
 'Panama': 'PAN',
 'Papua New Guinea': 'PNG',
 'Paraguay': 'PRY',
 'Peru': 'PER',
 'Philippines': 'PHL',
 'Pitcairn': 'PCN',
 'Poland': 'POL',
 'Puerto Rico': 'PRI',
 'Qatar': 'QAT',
 'Réunion': 'REU',
 'Romania': 'ROU',
 'Russian Federation': 'RUS',
 'Rwanda': 'RWA',
 'Saint Barthélemy': 'BLM',
 'Saint Helena': 'SHN',
 'Saint Kitts and Nevis': 'KNA',
 'Saint Lucia': 'LCA',
 'Saint Martin(French part)': 'MAF',
 'Saint Pierre and Miquelon': 'SPM',
 'Saint Vincent and the Grenadines': 'VCT',
 'Samoa': 'WSM',
 'San Marino': 'SMR',
 'Sao Tome and Principe': 'STP',
 'Saudi Arabia': 'SAU',
 'Senegal': 'SEN',
 'Serbia': 'SRB',
 'Seychelles': 'SYC',
 'Sierra Leone': 'SLE',
 'Singapore': 'SGP',
 'Sint Maarten(Dutch part)': 'SXM',
 'Slovakia': 'SVK',
 'Slovenia': 'SVN',
 'Solomon Islands': 'SLB',
 'Somalia': 'SOM',
 'South Africa': 'ZAF',
 'South Georgia and the South Sandwich Islands': 'SGS',
 'South Sudan': 'SSD',
 'Sri Lanka': 'LKA',
 'Sudan': 'SDN',
 'Suriname': 'SUR',
 'Svalbard and Jan Mayen Islands': 'SJM',
 'Sweden': 'SWE',
 'Switzerland': 'CHE',
 'Syrian Arab Republic': 'SYR',
 'Taiwan, Province of China': 'TWN',
 'Tajikistan': 'TJK',
 'United Republic of Tanzania': 'TZA',
 'Thailand': 'THA',
 'Timor-Leste': 'TLS',
 'Togo': 'TGO',
 'Tokelau': 'TKL',
 'Tonga': 'TON',
 'Trinidad and Tobago': 'TTO',
 'Tunisia': 'TUN',
 'Türkiye': 'TUR',
 'Turkmenistan': 'TKM',
 'Turks and Caicos Islands': 'TCA',
 'Tuvalu': 'TUV',
 'Uganda': 'UGA',
 'Ukraine': 'UKR',
 'United Arab Emirates': 'ARE',
 'United States of America': 'USA',
 'United States Minor Outlying Islands': 'UMI',
 'Uruguay': 'URY',
 'Uzbekistan': 'UZB',
 'Vanuatu': 'VUT',
 'Bolivarian Republic of Venezuela': 'VEN',
 'Viet Nam': 'VNM',
 'Virgin Islands(US)': 'VIR',
 'Wallis and Futuna Islands': 'WLF',
 'Western Sahara': 'ESH',
 'Yemen': 'YEM',
 'Zambia': 'ZMB',
 'Zimbabwe': 'ZWE'
 }

client = MongoClient("mongodb://mongodb:XNOVA100amazonaws@63.34.79.241:27017/xnova")  
database = client["xnova"] 

ACCESS_KEY = st.secrets["AWS"]["ACCESS_KEY_ID"]
SECRET_KEY = st.secrets["AWS"]["SECRET_ACCESS_KEY"]

bedrock = boto3.client('bedrock-runtime',aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name="us-east-1")

api_url = " https://umoe90xbt8.execute-api.eu-west-1.amazonaws.com/test/europe_category_searcher"

def judge_Llama3(query, description, terms):
    user_message= f"""
    You will receive a query, a list of terms, and a description of a company. Your task is to determine if the description directly addresses the query and includes the listed terms.
    You should provide a reason why it does or does not directly address the query and include the terms."\n 

    Query: {query} \n
    Terms: {terms} \n
    Description: {description} \n

    Begin your answer with "Yes" or "No" depending on your conclusion. 
    """

    prompt = f"""
    <|begin_of_text|>
    <|start_header_id|>user<|end_header_id|>
    {user_message}
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """
    body = json.dumps({
        "prompt": prompt,
        "temperature": 0.0,
        "top_p": 1.0,
        "max_gen_len": 500
    })
    try:
        modelId = "meta.llama3-70b-instruct-v1:0"
        response = bedrock.invoke_model(
            body=body,
            modelId=modelId,
        )
        response_body = json.loads(response['body'].read())
        text_generated = response_body["generation"]

        return text_generated
        
    except Exception as e:
        print(e)
        return ''

def process_description(id, query, terms):
    europe_products_descr = database["europe_products_descr"]
    description = europe_products_descr.find_one({'id':id})['description']
    response = judge_Llama3(query, description, terms)
    match = re.search(r"\b(Yes|No)\b(.*)", response, re.IGNORECASE | re.DOTALL)

    explanation = ''
    if match:
        decision_word = match.group(1)
        explanation = match.group(2).strip()
        if decision_word.lower() == "yes":
            return True, description, explanation  
    return False, description, explanation

def titan_embeddings(producto, client=bedrock):
    producto = producto.lower()
    modelId = "amazon.titan-embed-text-v1"
    body = json.dumps({"inputText": producto})
    accept = "application/json"
    contentType = "application/json"

    try:
        response = client.invoke_model(
            body=body,
            modelId=modelId,
            accept=accept,
            contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        embedding = response_body.get('embedding')
        return embedding

    except Exception as e:
        print(e)
        sys.exit()

def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)

def get_companies():
    terms_countries = st.session_state['terms']
    terms = [term for term, country in terms_countries ]
    countries = [country for term, country in terms_countries ]
    if 'ALL' in countries:
        countries = all_countries
    document = {
        "terms": terms,
        "countries": countries,
        "isSearch":True
    }
    response = requests.post(api_url, json=document)
    response = response.json()
    companies = response.get('companies')
    st.session_state['terms'] = []

    return companies

def process_candidate(scores, id, text, terms):
    score = scores[id]
    veredict, description, explanation = process_description(id, text, terms)
    id_descr = str(description)
    if veredict:
        score += 100

    return id, score, id_descr, explanation

def search_candidate(document, text_emb):
    _id = document['id']
    doc_embedding = document['descr_embedding']
    similarity = cosine_similarity(np.array(text_emb), np.array(doc_embedding))
    if similarity > 0.50: 
        return True, _id, similarity
    else: 
        return False, _id, similarity
        

def descr_search(text, df):
    europe_products_descr = database["europe_products_descr"]
    text_emb = titan_embeddings(text)
    ids = df['id'].tolist()
    candidates = europe_products_descr.find({'id':{'$in':ids}})
    scores = {}
    # buscar posibles candidatos
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(search_candidate, document, text_emb) for document in candidates]
        for future in as_completed(futures):
            res, _id, similarity = future.result()
            if res:
                scores[_id] = similarity

    # Procesar solo el diccionario y luego añadir al dataframe
    terms = st.session_state['query_terms']
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_candidate, scores, id, text, terms) for id in scores.keys()]
        for future in as_completed(futures):
            id, score, id_descr, explanation = future.result()
            df.loc[df['id'] == id, 'score'] = score
            df.loc[df['id'] == id, 'description'] = id_descr
            df.loc[df['id'] == id, 'explanation'] = explanation          

    df = df.sort_values(by='score', ascending=False) 
    return df

def add_term(item, country):
    item = item.lower()
    item = item.capitalize()

    if (item, country) not in st.session_state['terms']:
        st.session_state['terms'].append((item, country))
        st.session_state['query_terms'] = st.session_state['terms']

    res = '\n'
    for term, country in st.session_state['terms']:
        res += f'{term} {country} \n'

    st.text(f"ADDED: {res}")
    st.session_state['data'] = pd.DataFrame()

def clear():
    st.session_state['terms'] = []
    st.session_state['query_terms'] = []
    st.session_state['data'] = pd.DataFrame()

def run_app():
    columns = ['id', 'name', 'address', 'turnover', 'employees', 'categories', 'score', 'website', 'products', 'description', 'explanation']

    if 'terms' not in st.session_state:
       st.session_state['terms'] = []
    
    if 'query_terms' not in st.session_state:
        st.session_state['query_terms'] = []

    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=columns)
     
    st.title('Product Searcher')

    col1, col2 = st.columns(2)
    
    with col1:
        item_buscar = st.text_input("INTRODUCE A KEYWORD:")
    
    with col2:
        country = countries[st.selectbox('SELECT COUNTRY:', list(countries.keys()))]
    
    col3, col4, col5, col6, col7, col8 = st.columns(6)

    with col3:
        add_button = st.button('add')
    if add_button:
        if item_buscar:
            add_term(item_buscar, country)
    with col4:
        clear_button = st.button('clear')
        if clear_button:
            clear()
    
    with col6:
        search_but = st.button('search')

    # Create a placeholder for the DataFrame
    df_placeholder = st.empty()

    if search_but:
        companies = get_companies()

        if companies:
            st.session_state['data'] = pd.DataFrame(companies, columns=columns)

    if not st.session_state['data'].empty:
        df_placeholder.dataframe(st.session_state['data'])

        buscar_descripcion = st.text_input("ADVANCED SEARCH:")
        if buscar_descripcion:
            print("Buscando...")
            st.session_state['data'] = descr_search(buscar_descripcion, st.session_state['data'])
            df_placeholder.dataframe(st.session_state['data'])
            # st.session_state['terms'] = []
            # st.session_state['data'] = pd.DataFrame(columns=columns)

if __name__ == "__main__":
    run_app()