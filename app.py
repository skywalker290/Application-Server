from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin
from flask import Flask, send_file, jsonify
from functions import *
# from stable_diffusion_2 import * 
from stable_diffusion_xl_turbo import *

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
    return gen_json(sdxl_turbo(request))

@app.route('/get-file/<user>/<filename>', methods=['GET'])
def get_file(user,filename):
    filename= f"CardjiImages/{user}/{filename}" 
    return send_file(filename, as_attachment=True)

@app.route('/delimage', methods=['POST'])
def del_file(): 
    check = check_credentials(request)
    if(check != True):
        return check
    return delete_files(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
