
import requests     
key = 'iAzsAQrxRlDO9OJE7KC2L4ONj3sBm3Mk' 
url = 'https://openapi.taptools.io/api/v1' 
snek = '279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f534e454b'  
r = requests.get( 
    f'{url}/token/ohlcv',
    params={'unit': snek,
     'interval': '1d'},    
     headers={'x-api-key': key} ) 
print(r.json())


