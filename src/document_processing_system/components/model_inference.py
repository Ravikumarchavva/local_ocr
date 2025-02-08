import os
import torch
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from config.purpose.dps_qc_report_config import get_qc_prompt

class ModelInference:
    def __init__(self, model_name):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True, 
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            quantization_config=bnb_config,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.output_folder = "qc_reports_14b"
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_json_output(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs)
        
        # Decode and clean up response
        response = self.tokenizer.decode(outputs[0])
        return response

    def process_pages(self, final_items):
        responses = []
        for i, page in enumerate(tqdm(final_items, desc="Processing Pages", unit="page")):
            prompt = get_qc_prompt(page)  # Get structured prompt
            response = self.generate_json_output(prompt)  # Ask model directly for JSON
            responses.append(response)
            if i > 1:
                break
            # Save JSON output
            # output_path = os.path.join(self.output_folder, f"qc_report_page_{i}.json")
            # with open(output_path, "w", encoding="utf-8") as json_file:
            #     json.dump(response, json_file, indent=4, ensure_ascii=False)

            # print(f"Saved: {output_path}")
        return responses

if __name__ == '__main__':
    model_name = "Qwen/Qwen2.5-14B"
    model_inference = ModelInference(model_name)
    final_items = [...]  # Replace with actual final_items
    responses = model_inference.process_pages(final_items)
    for response in responses:
        print(response)