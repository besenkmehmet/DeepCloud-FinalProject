import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition, FaceAttributes
from upload_image import upload_blob

KEY = "59b178b172ae40938f6ce607f539b8ff"
ENDPOINT = "https://31313131.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))



#function to convert PIL image to png
def convertToPNG(im):
    with BytesIO() as f:
        im.save(f, format='PNG')
        return f.getvalue()



def detect_faces(face_image_url):

    #read image from url and store as PIL image
    response = requests.get(face_image_url)
    img = Image.open(BytesIO(response.content))

    #to draw on the image
    bounding_boxed_img = ImageDraw.Draw(img)

    #send the image to azure and fetch detected faces
    detected_faces = face_client.face.detect_with_url(url=face_image_url, detection_model='detection_03',return_face_landmarks=True, return_face_attributes=['headpose','mask'])
    
    if not detected_faces:
        print("No face detected!")


    mask_count = 0
    face_count = len(detected_faces)
    faces = []

    for face in detected_faces: 

        hasMask =  face.face_attributes.mask.type == "faceMask"
        nose_and_mouth_covered =  face.face_attributes.mask.nose_and_mouth_covered

        outline_color = "red"


        if hasMask:
            mask_count += 1
            outline_color = "green"

        face_rect = face.face_rectangle
        
        top = face_rect.top
        left = face_rect.left
        width = face_rect.width
        height = face_rect.height


        x0,y0 = left, top
        x1,y1 = left+width , top+height
        
        bounding_boxed_img.rectangle([x0,y0,x1,y1], fill =None , outline =outline_color ,width=4)


        faces.append([face.face_id,hasMask,nose_and_mouth_covered])

    url = upload_blob(convertToPNG(img))

    return (url,face_count, mask_count,faces)