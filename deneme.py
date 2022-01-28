import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

container_name = "cmpe363-blob"
blob_name = "Screenshot_3.png"

try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
    connect_str = """DefaultEndpointsProtocol=https;AccountName=cmpe361store;AccountKey=xJ5lwwBRe7nEClJ7loQdsoyR2T8RW/1QcOe+T73ngTzq7MHZPHzYDpbz5H3llbNeIupIvU6/rpm35+uLAoMMKg==;EndpointSuffix=core.windows.net"""
    # Quick start code goes here


    # Create a blob client using the local file name as the name for the blob
    blob_service_client  = BlobServiceClient.from_connection_string(connect_str)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)


    # Upload the created file
    with open("./Screenshot_2.png", "rb") as data:
        a = blob_client.upload_blob(data)
        print(a)

except Exception as ex:
    print('Exception:')
    print(ex)