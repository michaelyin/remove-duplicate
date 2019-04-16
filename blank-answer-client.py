import requests
from os import listdir
from os.path import join
from PIL import Image
import time
import cv2

API_URL = 'http://localhost:8686/answer/blank'
request_time = []
img_base_dir = '/document/ocr/images/'


def predict_result(image_path):
    # Initialize image path
    start = time.time()
    image = open(image_path, 'rb').read()
    payload = {'image': image}

    # Submit the request.
    r = requests.post(API_URL, files=payload).json()
    request_time.append(time.time() - start)
    return r


img_path = img_base_dir + '1517038814899.png'
img_path = img_base_dir + '1492430406371.png'
#img_path = "/home/michael/workspace-usa/OCRCloud/WyunOcrClient/src/test/resources/tifimages/2015-10-13_11_35_40.tif"

image = cv2.imread(img_path)
cv2.imshow('ocr', image)


result = predict_result(img_path)


print result

cv2.waitKey(0)
cv2.destroyAllWindows()