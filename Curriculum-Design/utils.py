import base64
from PIL import Image, ImageOps
import io
import requests
import xml.etree.ElementTree as ET

def encode_photo_to_base64(photo_path):
    with Image.open(photo_path) as img:
        img = crop_and_resize_image(img)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

def crop_and_resize_image(img):
    # Crop the image to a square and resize to 64x64
    img = ImageOps.fit(img, (64, 64), Image.LANCZOS)
    return img

def fetch_random_photo():
    url = 'https://www.thispersondoesnotexist.com/'
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        img_path = 'random_photo.png'
        img.save(img_path)
        return img_path
    else:
        raise Exception("Failed to fetch random photo")

def save_xml_tree(tree, file_path):
    tree.write(file_path, encoding="utf-8", xml_declaration=True)
