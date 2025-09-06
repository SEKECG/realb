import os
import sys
import argparse
import torch
from PIL import Image
from multiprocessing import Process, Queue
from model_handlers import JoyCaptionHandler, MoLMoHandler, MoLMo72bHandler, Qwen2VLHandler, PixtralHandler, Idefics3Handler, ExLLaMA2Handler, LlavaHandler, MiniCPMoHandler, GenericModelHandler
from utils import measure_gpu_speed, resize_image_proportionally
from image_processor import process_image_worker, get_handler, get_torii03_user_prompt, get_torii04_system_prompt, get_torii04_user_prompt
from arg_parser import check_mutually_exclusive, parse_arguments

def split_extension(filename):
    return os.path.splitext(filename)

def main():
    args = parse_arguments()
    check_mutually_exclusive(args, ['model_name_or_path', 'input_model_type'])

    input_dir = args.input_dir
    model_name_or_path = args.model_name_or_path
    input_model_type = args.input_model_type
    gpu_ids = args.gpu_ids
    output_extension = args.output_extension
    caption_format = args.caption_format

    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        sys.exit(1)

    image_files = [f for f in os.listdir(input_dir) if split_extension(f)[1].lower() in ['.jpg', '.png', '.webp', '.jpeg']]
    total_files = len(image_files)

    job_queue = Queue()
    result_queue = Queue()

    for image_file in image_files:
        job_queue.put(os.path.join(input_dir, image_file))

    processes = []
    for i, gpu_id in enumerate(gpu_ids):
        p = Process(target=process_image_worker, args=(i, gpu_id, job_queue, result_queue, model_name_or_path, input_model_type, vars(args), total_files))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    while not result_queue.empty():
        result = result_queue.get()
        print(result)

if __name__ == "__main__":
    main()