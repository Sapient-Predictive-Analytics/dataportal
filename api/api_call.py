import requests     
key = 'yourAPIkeyHERE' 
url = 'https://openapi.taptools.io/api/v1' 
wmt = '1d7f33bd23d85e1a25d87d86fac4f199c3197a2f7afeb662a0f34e1e776f726c646d6f62696c65746f6b656e'  
r = requests.get( 
    f'{url}/token/ohlcv',
    params={'unit': wmt,
     'interval': '1d'},    
     headers={'x-api-key': key} ) 
print(r.json())


