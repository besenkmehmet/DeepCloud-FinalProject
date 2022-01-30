import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import uuid
from dotenv import load_dotenv


load_dotenv()


container_name = os.environ.get("CONTAINER_NAME")
connect_str = os.environ.get("CONTAINER_CONN_STRING")
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