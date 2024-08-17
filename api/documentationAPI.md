## CSV - API for Native Token Data / Ingest Data Feeds into Zipline and Backtrader Programs

### Usage

* Download [api-call-script.py](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/api/api-call-script.py) from this folder of the repository to your environment
  
* Make sure to replace "your_api_key_here" with **your actual API key** in the script.

Run the script in your linux terminal with desired updating period.
Replace **ticker** with any of the available tickers AGIX, BOOK, COPI, GENS, IAG, INDY, LENFI, MELD, MIN, MILK, NEWM, NTX, SNEK, SUNDAE, WMT, WRT


To get all data: 
~~~
python3 api-call-script.py ticker.csv
~~~

To get the last day's data: 
~~~
python3 api_call.py ticker.csv day
~~~

To get the last 7 trading days' data: 
~~~
python3 api_call.py ticker.csv week
~~~

To get the last 14 trading days' data: 
~~~
python3 api_call.py ticker.csv fortnight
~~~

To get **custom strategy data**, get the ticker of the strategy from our community or social media pages for example instead of WMT.csv for World Mobile Token, use S81.csv for strategy #81 if you are aware that the signal exists.


### Motivation
As part of the Dataportal we like to provide a simple, free and lightweight API to allow users to download selected, cleaned Cardano native token time series data stored in the cloud. The first step is a minimal viable solution using open-source tools and a major cloud provider like AWS or Google with later optimization and redundancies possible.

This consists of initially four components:

1. Cloud Storage with AWS S3 or Google Cloud Storage to store our data.
2. API Framework: Python-based FastAPI that is easy to use and generates OpenAPI specs automatically
3. Cloud Hosting AWS Lambda or Google Cloud Functions to provide a serverless model
4. Client Script: Catalyst/Cardano users can execute simple Python script on their machine using the [requests](https://pypi.org/project/requests/) library

### Cloud Storage

### API Framework
To access WMT token prices the following Lambda code will be provided:

~~~
import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'sapientassets'
    file_name = 'WMT.csv'
    
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = response['Body'].read().decode('utf-8')
        return {
            'statusCode': 200,
            'body': json.dumps({'data': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
~~~

### Cloud Hosting

### Client Script
Download or touch file and execute in your terminal:

~~~
import requests
import sys

def main():
    api_url = "https://gwsl86ibha.execute-api.us-east-1.amazonaws.com/data"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()['data']
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
~~~

The API has been deployed on *https://gwsl86ibha.execute-api.us-east-1.amazonaws.com* and is ready for integration with Backtesting in the next Milestone.

![SapientGateway](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/api/api_gateway.jpg)

Token data for 16 native token tickers AGIX, BOOK, COPI, GENS, IAG, INDY, LENFI, MELD, MIN, MILK, NEWM, NTX, SNEK, SUNDAE, WMT, WRT is available and custom signals will be added once the portal goes live and as requested by the community.

![Uploads](https://github.com/Sapient-Predictive-Analytics/dataportal/blob/main/api/Screenshot%20(201).png)
