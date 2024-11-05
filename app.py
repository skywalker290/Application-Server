from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin
from flask import Flask, send_file, jsonify
from functions import *
from stable_diffusion_2 import * 

app = Flask(__name__, static_url_path='/Output_images')
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

@app.route("/")
def hello():
    return gen_json("Helloo There Flux here!")

@app.route('/genimage', methods = ['POST'])
def generate_image():
    check = check_credentials(request)
    if(check != True):
        return check
    return gen_json(sd2(request))

@app.route('/get-file/<filename>', methods=['GET'])
def get_file(filename):
    filename='Output_images/'+filename 
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

