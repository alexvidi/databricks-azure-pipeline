import sys
import os

# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from azure.storage.blob import BlobServiceClient
from src.config import load_config

def test_azure_connection():
    """Test connection to Azure Blob Storage."""
    config = load_config()
    
    try:
        # Create BlobServiceClient using account name and key
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={config['storage_account_name']};AccountKey={config['storage_account_key']};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # List containers in the storage account
        containers = blob_service_client.list_containers()
        print("Successfully connected to Azure Blob Storage. Available containers:")
        for container in containers:
            print(f"- {container['name']}")
    
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    test_azure_connection()
