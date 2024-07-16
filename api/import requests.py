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