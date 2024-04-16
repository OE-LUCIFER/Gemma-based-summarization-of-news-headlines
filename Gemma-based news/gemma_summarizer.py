import time
import os

import torch

from summarizer import Summarizer

from transformers import AutoTokenizer, AutoModelForCausalLM

class GemmaSummarizer(Summarizer):
    def __init__(self, hf_token: str = "your_hf_token_here", device: str = "cpu"):
        self.model = Summarizer()

        self.device = device
        self.hf_token = hf_token

        self._load_gemma_model()

    def _load_gemma_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-1.1-2b-it", token=self.hf_token)
        self.model = AutoModelForCausalLM.from_pretrained("google/gemma-1.1-2b-it", token=self.hf_token)

        if self.device != "cpu":
            self.model = self.model.half()
            self.model.to(self.device)

    def _prepare_prompt(self, text: str):
        prompt = "<start_of_turn>user\n"
        prompt += "Here is the original text:\n"
        prompt += text
        prompt += "\nnPlease write a narrative summary of this article for me."
        prompt += "\n<end_of_text>\n"
        prompt += "<start_of_turn>model\n"

        return prompt

    def summarize(self, text: str, max_length: int = 512):
        start_time = time.time()

        prompt = self._prepare_prompt(text)

        with torch.no_grad():
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
            input_ids = input_ids.to(self.device)
            output = self.model.generate(input_ids, 
                                         max_length=input_ids.size(1)+max_length, 
                                         do_sample=False, 
                                         temperature=0.9)
            output_text = self.tokenizer.decode(output[0], skip_special_tokens=False)

        # from `output_text`, take out the model's response wrapped in <start_of_turn>model and <end_of_turn>.
        model_response = output_text.split("<start_of_turn>model")[1].split("<end_of_turn>")[0].strip()
        # remove `<eos>` token
        model_response = model_response.replace('<eos>', '')

        elapsed_time = time.time() - start_time
        return model_response, elapsed_time

