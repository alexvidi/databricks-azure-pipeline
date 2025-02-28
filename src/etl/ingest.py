
import sys
import os
# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import requests
import json
from azure.storage.blob import BlobServiceClient
from src.config import load_config

def fetch_data_from_api():
    """Fetch product data from DummyJSON API."""
    url = "https://dummyjson.com/products"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["products"]
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def save_data_to_blob(data, filename):
    """Save JSON data to Azure Blob Storage."""
    config = load_config()

    # Create BlobServiceClient
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={config['storage_account_name']};AccountKey={config['storage_account_key']};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get container client
    container_client = blob_service_client.get_container_client(config["container_name"])

    # Convert data to JSON string
    json_data = json.dumps(data, indent=4)

    # Upload data to Blob Storage
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(json_data, overwrite=True)

    print(f"Data successfully uploaded to Azure Blob Storage as {filename}")

if __name__ == "__main__":
    print("Fetching data from API...")
    data = fetch_data_from_api()

    if data:
        print("Uploading data to Azure Blob Storage...")
        save_data_to_blob(data, "raw-data/products.json")
