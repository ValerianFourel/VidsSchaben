import torch
from transformers import PaliGemmaForConditionalGeneration, AutoProcessor
from PIL import Image
import requests

class PaliGemma:
    def __init__(self, model_id="google/paligemma-3b-mix-224", max_new_tokens=1000):
        self.model = PaliGemmaForConditionalGeneration.from_pretrained(model_id)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.max_new_tokens = max_new_tokens

    def run(self, task, image_path):
        image = Image.open(image_path)
        # image = Image.open(requests.get(image_url, stream=True).raw)
        inputs = self.processor(task, image, return_tensors="pt")
        output = self.model.generate(**inputs, max_new_tokens=self.max_new_tokens)
        return self.processor.decode(output[0], skip_special_tokens=True)[len(task):]

# Usage example:
# model = SimplePaliGemma()
# result = model.run("Describe this image:", "https://example.com/image.jpg")
# print(result)
