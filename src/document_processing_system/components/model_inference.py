import os
import json
import torch
import logging  # added logging import
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline  # added pipeline
from utils.post_processing import extract_json_objects
from config.purpose.dps_qc_report_config import get_qc_prompt
from config.settings import DATA_DIR

logging.basicConfig(level=logging.INFO)  # basic configuration

class ModelInference:
    def __init__(self, model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # BitsAndBytesConfig for 4-bit quantization
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True, 
            bnb_4bit_compute_dtype=torch.bfloat16
        )

        logging.info("Loading model and tokenizer...")  # replaced print
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            quantization_config=bnb_config
        ).to(self.device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        
        # Create pipeline for text generation
        self.llm_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )
        
        logging.info("Model loaded successfully!")  # replaced print

    def generate_json(self, text):
        """Generates JSON output from the model given an input text."""
        # Use pipeline instead of model.generate
        outputs = self.llm_pipeline(
            text,
            max_new_tokens=4096
        )
        # Pipeline's result is a list with a 'generated_text' key
        response = outputs[0]["generated_text"]

        # if len(response) > len(text):
        #     response = response[len(text):]

        json_response = extract_json_objects(response)

        return json_response

    def process_items(self, items, output_folder=None):
        """Processes a list of extracted items and saves JSON output for each."""
        if output_folder is None:
            output_folder = os.path.join(DATA_DIR, 'qc_data', 'qc_reports_output', 'qc_reports_14b')
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

            logging.info(f"Saved: {output_path}")  # replaced print

        return responses