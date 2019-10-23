# import needed modules
import requests
import numpy as np
import pandas as pd

# for regex
import re


def get_geolocation_from_ip(ip):
    """
    Returns json data or None if invalid IP address
    
    We use https://ipgeolocationapi.com/
    """
    data = None
    
    request = requests.get("https://api.ipgeolocationapi.com/geolocate/{}"
                           .format(ip))
    
    if request:
        data = request.json()
    
    return data


if __name__ == '__main__':
    
    # load csv file into pandas DataFrame
    products = pd.read_csv('products.csv', sep=';')
    
    # build 'currency_code' column
    products['currency_code'] = [r['currency_code'] if r else None
                                 for r in [get_geolocation_from_ip(ip) 
                                           for ip in products['ip_address']]]

    # exchange rate to EUR
    exchange_rate_to_eur = requests.get(
        "https://api.exchangerate-api.com/v4/latest/EUR").json()
    #exchange_rate_to_eur = requests.get("https://api.ratesapi.io/api/latest").json()
    #exchange_rate_to_eur = requests.get("https://api.exchangeratesapi.io/latest").json()

    # build 'rate_to_euro' column
    products['rate_to_euro'] = [exchange_rate_to_eur['rates'][c]
                                if c in exchange_rate_to_eur['rates']
                                else None
                                for c in products['currency_code']]

    # Work on a copy
    df = products.copy()

    # drop NaN
    df = df.dropna()

    # convert price to float
    df['price'] = pd.to_numeric(df.price, errors='coerce')

    # create a new column with price in euros
    df['price_in_euro'] = df['price'] / df['rate_to_euro']

    # Make the list of ingredients
    df2 = df.copy()

    # pattern for keeping only alphanumeric character
    pattern = re.compile('[^a-zA-Z0-9]')

    # Create new column  from 'infos'
    # 1. convert to lower case
    # 2. remove punctuation
    # 3. split in a list
    # 4. Drop empty strings
    df2['info_as_list'] = df2.infos \
        .str.lower() \
        .apply(lambda w: pattern.sub(" ", w)) \
        .str.split() \
        .apply(lambda cell: list(filter(None, cell)))

    # get list of unique words
    results = set()
    df2['info_as_list'].apply(results.update)
    ingredients = list(results)

    # remove non ingredients from the list
    stop = ['may', 'contains', 'and', 'contain', 'ingredients']

    pattern = re.compile(r'|'.join(stop))
    ingredients = [ingredient for ingredient in [pattern.sub("", w) for w in ingredients]
                   if ingredient]

    print(ingredients)
    
    for ingredient in ingredients:
        df2[ingredient] = df2.info_as_list.apply(lambda cell: ingredient in cell)
    
    print(df2.head())

    print("That's All, Folks!")
