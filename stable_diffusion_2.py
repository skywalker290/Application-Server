from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from functions import gen_name
from dotenv import load_dotenv
import os

load_dotenv()

PUBLIC_IP = os.getenv('PUBLIC_IP')

model_id = "stabilityai/stable-diffusion-2"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
sd2_model = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
sd2_model = sd2_model.to("cuda")

def sd2(request):
    
    data = request.get_json()
    prompt = data.get('prompt')
    height = data.get('height')
    width = data.get('width')
    
    output_image_file = f'{gen_name()}.png'
    output_image_path = f'Output_images/{output_image_file}'

    image = sd2_model(prompt, height=height, width=width).images[0]
    image.save(output_image_path)
    
    return f"http://{PUBLIC_IP}/get-file/{output_image_file}"


