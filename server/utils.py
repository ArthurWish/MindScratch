from base64 import b64decode, b64encode
from PIL import Image
from io import BytesIO
import io
import base64
import requests
from rembg import remove

def rm_img_bg_local(in_path, out_path):
    with open(in_path, 'rb') as i:
        with open(out_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)
    with open(out_path, 'rb') as o:
        encoded_data = base64.b64encode(o.read())
        return encoded_data.decode('utf-8')

def extract_block_types(data):
    block_types = []
    for block in data:
        block_types.append(block['block_type'])
        if 'substack' in block:
            block_types.extend(extract_block_types(block['substack']))
        if 'arguments' in block:
            for arg in block['arguments'].values():
                if isinstance(arg, dict) and 'block_type' in arg:
                    block_types.extend(extract_block_types([arg]))
    return block_types