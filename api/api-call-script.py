import requests
import sys
import json

# Base Invoke URL (ends with /prod)
BASE_URL = "https://pfc4s34m21.execute-api.ap-southeast-1.amazonaws.com/prod"
# Resource path
RESOURCE_PATH = "/csv"
# Full API endpoint
API_ENDPOINT = BASE_URL + RESOURCE_PATH

# API Key (replace with your actual API key)
API_KEY = "your_api_key_here"

def get_csv_data(file_name, period='all'):
    print(f"Attempting to access file: {file_name}")
    print(f"Period: {period}")
    print(f"Using API endpoint: {API_ENDPOINT}")
    
    headers = {
        "x-api-key": API_KEY
    }
    
    params = {
        'file': file_name,
        'period': period
    }
    
    try:
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=10)
        
        print(f"Request URL: {response.url}")
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
        
        if response.status_code == 200:
            print("Success! Here's the response:")
            print(response.text)
        elif response.status_code == 403:
            print("Error: Invalid or missing API key")
        elif response.status_code == 404:
            error_data = response.json()
            print(f"Error: File '{file_name}' not found")
            print("Available files in the bucket:")
            for file in error_data.get('available_files', []):
                print(f"- {file}")
        else:
            print(f"Error: Unexpected status code: {response.status_code}")
            print("Response content:")
            print(response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 api_call.py <file_name> [period]")
        print("Period can be 'day', 'week', 'fortnight', or 'all' (default)")
        sys.exit(1)
    
    file_name = sys.argv[1]
    period = sys.argv[2] if len(sys.argv) == 3 else 'all'
    
    get_csv_data(file_name, period)
