import requests
import urllib.parse as ulib
from flask import Flask,jsonify,request
from requests.structures import CaseInsensitiveDict


app = Flask(__name__)
QUERY_URL = "https://api.openai.com/v1/images/generations"
def generate_image(prompt, model, api_key):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    api_key = "Bearer " + api_key

    headers["Authorization"] = api_key

    model = model
    prompt = prompt

    model_engine = "image-alpha-001"
    data = """
    {
        """
    data += f'"model": "{model_engine}",'
    data += f'"prompt": "{prompt}",'
    data += """
        "num_images":1,
        "size":"1024x1024",
        "response_format":"url"
    }
    """

    resp = requests.post(QUERY_URL, headers=headers, data=data)

    if resp.status_code != 200:
        return False

    response_text = json.loads(resp.text)
    return response_text['data'][0]['url']


@app.route('/',methods = ['GET'])
def dalle():
    prompt = ulib.unquote(request.args.get('prompt',1))
    api_key = request.args.get('api_key',1)
    img_url = generate_image(prompt,'image-alpha-001',api_key)
    if not img_url:
        data = {
          'ok': False,
          'message': 'Cant generate image'
        }
        return jsonify()
    data = {
      'ok': True,
      'image_url': img_url
    }
    return jsonify(data)
