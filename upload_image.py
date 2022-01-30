import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import uuid

container_name = "cmpe363-blob"
connect_str = """DefaultEndpointsProtocol=https;AccountName=cmpe361store;AccountKey=xJ5lwwBRe7nEClJ7loQdsoyR2T8RW/1QcOe+T73ngTzq7MHZPHzYDpbz5H3llbNeIupIvU6/rpm35+uLAoMMKg==;EndpointSuffix=core.windows.net"""
# Create a blob client using the local file name as the name for the blob
blob_service_client  = BlobServiceClient.from_connection_string(connect_str)


def generateUUID():
    return str(uuid.uuid4())




def upload_blob(img):


    blob_name = generateUUID() + ".png"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)


    try:
        # Upload the created file
        # with open("./Screenshot_2.jpeg", "rb") as data:
        #     blob_client.upload_blob(data)
        blob_client.upload_blob(img)
        return str(blob_client.url)
    except Exception as ex:
        print('Exception:')
        print(ex)