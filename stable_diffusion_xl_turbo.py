from diffusers import AutoPipelineForText2Image
import torch
from functions import gen_name
from dotenv import load_dotenv
import os

load_dotenv()

PUBLIC_IP = os.getenv('PUBLIC_IP')

model_id = "stabilityai/sdxl-turbo"
sdxlt_model = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16")
sdxlt_model = sdxlt_model.to("cuda")

def sdxl_turbo(request):
    try:
        data = request.get_json()
        user = data.get('user')
        prompt = data.get('prompt')
        height = int(data.get('height'))
        width = int(data.get('width'))

        if((height % 8)!=0 or (width % 8)!=0):
            return "Height and Width must be a Multiple of 8", 500

        output_image_file = f'{gen_name()}.jpg'
        output_image_path = f'CardjiImages/{user}/{output_image_file}'

        directory = f"CardjiImages/{user}/"
        if not os.path.exists(directory):
            # Create the directory
            os.makedirs(directory)
            # print(f"Directory '{directory}' created.")
        else:
            print(f"Directory '{directory}' already exists.")

        image = sdxlt_model(prompt, height=height, width=width, num_inference_steps=1, guidance_scale=0.0).images[0]
        image.save(output_image_path)

        return f"http://{PUBLIC_IP}/get-file/{user}/{output_image_file}"

    except Exception as e:
        return ({"error": str(e)}), 500

