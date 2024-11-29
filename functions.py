import time
from flask import jsonify
from datetime import datetime
import os

def check_credentials(request):
    MY_KEY = "7865"
    data = request.get_json()

    if not data:
        return "Invalid request: No JSON payload found", 400

    KEY = data.get('KEY')

    if(KEY):
        if(KEY != MY_KEY):
            return "Authorization Failed [Incorrect Credentials]!", 401
    else:
        return "Authorization Failed [Key Not Found]!", 401
    
    return True

def gen_json(Data):
    response = {
        "data": Data
    }
    return jsonify(response)

def gen_name():
    return f"{int(time.time() * 1000)}"
    # return str(datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3])


def delete_files(request):
    data = request.get_json()
    paths = data['paths']
    deleted_files = []
    failed_files = []

    for file_path in paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(file_path)
            else:
                failed_files.append({"file": file_path, "error": "File does not exist."})
        except Exception as e:
            failed_files.append({"file": file_path, "error": str(e)})

    return jsonify({
        "deleted_files": deleted_files,
        "failed_files": failed_files
    })