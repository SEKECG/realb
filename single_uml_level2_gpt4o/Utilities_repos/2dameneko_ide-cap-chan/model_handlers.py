import torch
from transformers import AutoModel, AutoTokenizer, BitsAndBytesConfig

class ModelHandler:
    def __init__(self, model_name_or_path, device, args_dict):
        self.model_name_or_path = model_name_or_path
        self.device = device
        self.args_dict = args_dict
        self.model = None
        self.processor = None
        self.tokenizer = None
        self.quantization_config = self._get_quantization_config()
        self._initialize_model()

    def _get_quantization_config(self):
        if self.args_dict.get("quantization"):
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16
            )
        return None

    def _initialize_model(self):
        raise NotImplementedError("Subclasses should implement this method")

    def model_loader(self, model_name_or_path):
        return AutoModel.from_pretrained(model_name_or_path, quantization_config=self.quantization_config)

    def process_image(self, system_prompt, user_prompt, image):
        raise NotImplementedError("Subclasses should implement this method")

    def save_caption(self, caption, caption_path, encoding="utf-8", errors="ignore"):
        with open(caption_path, "w", encoding=encoding, errors=errors) as f:
            f.write(caption)


class JoyCaptionHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class MoLMoHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class MoLMo72bHandler(MoLMoHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class Qwen2VLHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class PixtralHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _get_quantization_config(self):
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16
        )

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class Idefics3Handler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class ExLLaMA2Handler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class LlavaHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class MiniCPMoHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass


class GenericModelHandler(ModelHandler):
    def __init__(self, model_name_or_path, device, args_dict):
        super().__init__(model_name_or_path, device, args_dict)

    def _initialize_model(self):
        self.model = self.model_loader(self.model_name_or_path)
        self.processor = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model.eval()

    def process_image(self, system_prompt, user_prompt, image):
        # Implement image processing and caption generation logic
        pass