import os
import json
import torch
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from utils.post_processing import extract_json_objects
from config.purpose.dps_qc_report_config import get_qc_prompt
from config.settings import DATA_DIR

class ModelInference:
    def __init__(self, model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # BitsAndBytesConfig for 4-bit quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True, 
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        print("Loading model and tokenizer...")
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            quantization_config=bnb_config
        ).to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        
        print("Model loaded successfully!")

    def generate_json(self, text):
        """Generates JSON output from the model given an input text."""
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=4096)

        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if len(response) > len(text):
            response = response[len(text):]

        json_response = extract_json_objects(response)

        return json_response

    def process_items(self, items, output_folder=DATA_DIR / 'qc_data' / 'qc_reports_output' / "qc_reports_14b"):
        """Processes a list of extracted items and saves JSON output for each."""
        os.makedirs(output_folder, exist_ok=True)

        responses = []
        for i, item in enumerate(tqdm(items, desc="Processing Items", unit="item")):
            prompt = get_qc_prompt(item)
            response = self.generate_json(prompt)
            responses.append(response)

            # Save JSON output
            output_path = os.path.join(output_folder, f"qc_report_item_{i}.json")
            with open(output_path, "w", encoding="utf-8") as json_file:
                json.dump(response, json_file, indent=4, ensure_ascii=False)

            print(f"Saved: {output_path}")

        return responses