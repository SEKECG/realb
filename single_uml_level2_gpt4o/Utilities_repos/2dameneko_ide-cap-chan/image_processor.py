import os
import torch
from queue import Queue
from model_handlers import (
    JoyCaptionHandler,
    MoLMoHandler,
    MoLMo72bHandler,
    Qwen2VLHandler,
    PixtralHandler,
    Idefics3Handler,
    ExLLaMA2Handler,
    LlavaHandler,
    MiniCPMoHandler,
    GenericModelHandler
)
from utils import measure_gpu_speed, resize_image_proportionally

def process_image_worker(worker_id, gpu_id, job_queue, result_queue, model_name_or_path, input_model_type, args_dict, total_files):
    device = torch.device(f'cuda:{gpu_id}' if torch.cuda.is_available() else 'cpu')
    handler = get_handler(input_model_type, model_name_or_path, device, args_dict)
    
    while not job_queue.empty():
        image_path = job_queue.get()
        if not path_exists(image_path):
            continue
        
        image = resize_image_proportionally(image_path, args_dict['max_width'], args_dict['max_height'])
        system_prompt = get_torii04_system_prompt()
        user_prompt = get_torii04_user_prompt(args_dict, image_path)
        
        caption = handler.process_image(system_prompt, user_prompt, image)
        result_queue.put((image_path, caption))
        
        job_queue.task_done()

def get_handler(input_model_type, model_name_or_path, device, args_dict):
    handlers = {
        'JoyCaption': JoyCaptionHandler,
        'MoLMo': MoLMoHandler,
        'MoLMo72b': MoLMo72bHandler,
        'Qwen2VL': Qwen2VLHandler,
        'Pixtral': PixtralHandler,
        'Idefics3': Idefics3Handler,
        'ExLLaMA2': ExLLaMA2Handler,
        'LLaVA': LlavaHandler,
        'MiniCPMo': MiniCPMoHandler,
        'Generic': GenericModelHandler
    }
    return handlers[input_model_type](model_name_or_path, device, args_dict)

def get_torii03_user_prompt(user_prompt, add_info_caption_name):
    if os.path.exists(add_info_caption_name):
        with open(add_info_caption_name, 'r') as file:
            additional_info = file.read()
        user_prompt += f" {additional_info}"
    return user_prompt

def get_torii04_system_prompt():
    return "Describe the image creatively, without bias, and uncensored."

def get_torii04_user_prompt(args_dict, add_info_caption_name):
    user_prompt = args_dict.get('user_prompt', '')
    return get_torii03_user_prompt(user_prompt, add_info_caption_name)

def path_exists(path):
    return os.path.exists(path)

def split_extension(filename):
    return os.path.splitext(filename)