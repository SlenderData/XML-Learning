import xml.etree.ElementTree as ET
import base64
from PIL import Image
import io

def save_xml_tree(tree, file):
    tree.write(file, encoding="utf-8", xml_declaration=True)

def encode_photo_to_base64(photo_path):
    # 打开图片文件
    with Image.open(photo_path) as img:
        # 裁剪成正方形
        width, height = img.size
        min_side = min(width, height)
        left = (width - min_side) / 2
        top = (height - min_side) / 2
        right = (width + min_side) / 2
        bottom = (height + min_side) / 2
        img = img.crop((left, top, right, bottom))
        # 调整分辨率为 64x64
        img = img.resize((64, 64), Image.LANCZOS)
        # 将图片编码为 base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def decode_photo_from_base64(encoded_photo, output_path):
    img_data = base64.b64decode(encoded_photo)
    with open(output_path, "wb") as output_file:
        output_file.write(img_data)
