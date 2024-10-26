import base64
import io
from flask import Flask, jsonify, request, make_response
import os
from flask_cors import CORS, cross_origin
import json
from PIL import Image
import requests
from prompt import *
from gpt import *
from image import generate_controlnet, generate_draw
from prompt_base import *
from utils import extract_block_types, rm_img_bg_local
from print_color import print

app = Flask(__name__)
CORS(app, resources=r"/*", supports_credentials=True, origins='*')
os.makedirs('./static', exist_ok=True)
os.makedirs('./static/images', exist_ok=True)
print(os.environ.get("HTTP_PROXY"))
print(os.environ.get("HTTPS_PROXY"))

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello'


@app.route('/api/extracted_subject', methods=['POST'])
def extracted_subject():
    user_input = request.json.get('user_input')
    agent = GPTTools(
        GPTType.gpt_4, "You are a helpful Scratch programming teacher. Answer in Chinese. The return format is JSON format.")
    response = agent.create_chat_completion(
        user_message=subject_extracted_prompt.format(input=user_input))
    response = json.loads(response)
    print("subject", response['subject'])
    return jsonify({'subject': response['subject']})


@app.route('/api/object_generation', methods=['POST'])
def object_generation():
    memory_dict = request.json.get('memory_dict')
    agent = GPTTools(
        GPTType.gpt_4, "You are a helpful Scratch programming teacher. Answer in Chinese. The return format is JSON format.")
    response = agent.create_chat_completion(
        user_message=object_generation_prompt.format(memory=memory_dict))
    response = json.loads(response)
    return jsonify({"object1": list(response["object1"].keys())[0],
                    "object2": list(response["object2"].keys())[0],
                    "object3": list(response["object3"].keys())[0]})


@app.route('/api/logic_extracted', methods=['POST'])
def logic_extracted():
    user_input = request.json.get('user_input')
    agent = GPTTools(
        GPTType.gpt_4, "You are a helpful Scratch programming teacher. Answer in Chinese. The return format is JSON format.")
    response = agent.create_chat_completion(
        user_message=logic_extracted_prompt.format(input=user_input))
    response = json.loads(response)
    return jsonify({"extracted_logic": response["extracted_logic"]})


@app.route('/api/logic_queries', methods=['POST'])
def logic_queries():
    user_input = request.json.get('user_input')
    agent = GPTTools(
        GPTType.gpt_4, "You are a helpful Scratch programming teacher. Answer in Chinese. The return format is JSON format.")
    response = agent.create_chat_completion(
        user_message=logic_queries_prompt.format(input=user_input))
    response = json.loads(response)
    return jsonify({"question1": response["question1"],
                    "question2": response["question2"],
                    "question3": response["question3"]})


@app.route('/api/comment_image', methods=['POST'])
def comment_image():
    base64_image = request.json.get('base64_image')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    return jsonify({'image_comment': response['choices'][0]['message']['content']})


@app.route('/api/new_object', methods=['POST'])
def new_object():
    try:
        object_memory = Memory(model=GPTType.gpt_4)
        memory_dict = request.json.get('memory_dict')
        if memory_dict is None:
            raise ValueError("Input the mind map")

        user_message = object_prompt.format(memory=memory_dict)
        response = object_memory.ask_gpt(user_message=user_message)
        print(response)

        response = json.loads(response)
        if isinstance(response["Generated_object"], dict):

            spriteName = list(response["Generated_object"].keys())[0]
            description = response["Generated_object"][spriteName]

            return jsonify({'spriteName': spriteName, 'description': description})
        else:
            return jsonify({'spriteName': response["Generated_object"], 'description': response["Generated_object"]})
    except Exception as e:
        print(e)


@app.route('/api/text_to_image', methods=['POST'])
def text_to_image():
    text = request.json.get('text')
    print("user_input", text)
    drawing_agent = GPTTools(
        GPTType.gpt_4, "Output in JSON format.")
    response = drawing_agent.create_chat_completion(
        user_message=drawing_prompt_new.format(drawing=text))
    response = json.loads(response)
    print("prompt", response['prompt'])
    image_base64 = generate_draw(response["prompt"], './static/text_image.png')
    if "type" in response.keys():
        if response["type"].lower() == "characters":
            image_base64 = rm_img_bg_local(
                "./static/text_image.png", "./static/rmbg_image.png")
            print("image background is remove!", tag='success',
                  tag_color='green', color='white')
    return jsonify({'image': image_base64})


@app.route('/api/image_to_image', methods=['POST'])
def image_to_image():
    print("image_to_image")
    text = request.json.get('text')  # user input
    print("user_input", text)
    image_base64 = request.json.get('user_image')  # base64
    if image_base64 is None:
        raise "image_base64 is none"
    base_img_bytes = base64.b64decode(image_base64)
    img = Image.open(io.BytesIO(base_img_bytes)).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255))
    combined = Image.alpha_composite(bg, img)
    combined.convert('RGB').save('./static/temp.png', 'PNG')
    drawing_agent = GPTTools(
        GPTType.gpt_4, "Output in JSON format.")
    response = drawing_agent.create_chat_completion(
        user_message=drawing_prompt_new.format(drawing=text))
    response = json.loads(response)
    print("prompt", response['prompt'])
    print(response["type"])
    image_base64 = generate_controlnet(
        prompt=response['prompt'], base_image="./static/temp.png")
    if "type" in response.keys():
        if response["type"].lower() == "characters":
            image_base64 = rm_img_bg_local(
                "./static/image_to_image.png", "./static/rmbg_image.png")
            print("image background is remove!", tag='success',
                  tag_color='green', color='white')
    return jsonify({'image': image_base64})


@app.route('/api/text_to_sound', methods=['POST'])
def text_to_sound():
    """ audio generate api version """
    api_url = 'http://127.0.0.1:5555/generate'
    prompt = request.json.get('prompt')
    if prompt == '':
        print("the sound is None", color="red")
        return
    sound_agent = GPTTools(
        GPTType.gpt_4, "Response in English. Output in JSON format.")
    response = sound_agent.create_chat_completion(
        user_message=sound_prompt.format(sound=prompt))
    response = json.loads(response)
    print("prompt", response['prompt'])
    headers = {'Content-type': 'application/json'}
    steps = 100
    data = {
        "prompt": response['prompt'],
        "steps": steps
    }
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        audio_data_b64 = response.json()['audio_data']
    return jsonify({'sound': audio_data_b64})


@app.route('/api/character_decomposition', methods=['POST'])
def character_decomposition():
    function_memory = Memory(model=GPTType.gpt_4)
    question = request.json.get('question')
    memory_dict = request.json.get('memory_dict')
    if memory_dict is None:
        raise "Input the mind map"
    print(question)
    print(memory_dict)
    user_message = function_prompt.format(
        question=question, memory=memory_dict)
    response = function_memory.ask_gpt(user_message=user_message)
    print("response", response)
    response = json.loads(response)
    if isinstance(response['function'], str):
        return jsonify({'answer': response['function']})
    spriteName = list(response["function"].keys())[0]
    _function = response["function"][spriteName]
    return jsonify({'answer': _function})


@app.route('/api/new_logic', methods=['POST'])
def new_logic():
    logic_memory = Memory(model=GPTType.gpt_4)
    question = request.json.get('question')
    memory_dict = request.json.get('memory_dict')
    if memory_dict is None:
        return "Input the mind map"
    user_message = logic_prompt.format(
        question=question, memory=memory_dict)
    response = logic_memory.ask_gpt(user_message=user_message)
    print("response", response)
    response = json.loads(response)
    return jsonify({'logic': response["logic"]})


@app.route('/api/generate_code', methods=['POST'])
def generate_code():
    logic = request.json.get('logic')
    memory_dict = request.json.get('memory_dict')
    if memory_dict is None:
        return "Input the mind map"
    agent = GPTTools(
        GPTType.gpt_4, "You are a Scratch programming expert. The return format is JSON format.")
    response = agent.create_chat_completion(
        user_message=code_prompt.format(user_input=logic))
    response = json.loads(response)
    print("code", response["code"])
    code = extract_block_types(response["code"])
    print(code)
    return jsonify({'code': code})


@app.route('/api/explain_code', methods=['POST'])
def explain_code():
    explain = request.json.get('explain')
    agent = GPTTools(
        GPTType.gpt_4, "You are a Scratch programming expert. The return format is JSON format.")
    response = agent.create_chat_completion(
        user_message=code_explain_prompt.format(code_block=explain["code_block"], p_theme=explain["p_theme"], p_role=explain["p_role"], p_logic=explain["p_logic"]))
    response = json.loads(response)
    return jsonify({'explain': response["explain"]})


@app.route('/api/extract_relation', methods=['POST'])
def extract_relation():
    nodes = request.json.get('nodes')
    agent = GPTTools(
        GPTType.gpt_4, "Please answear in Chinese."
    )
    response = agent.create_chat_completion(
        user_message=relation_prompt.format(node_1=nodes["node1"], node_2=nodes["node2"]))
    response = json.loads(response)
    return jsonify({'relationship': response["relationship"]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)
