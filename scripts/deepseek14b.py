from pathlib import Path
ROOT_DIR = Path().resolve().parent

pdf_dir = ROOT_DIR / 'data' / 'qc_templates'

import os

files = os.listdir(pdf_dir)
pdfs = [file for file in files if file.endswith('.pdf')]
pdf_path = pdf_dir / pdfs[-1]

import pdfplumber
from tqdm.auto import tqdm

def extract_text_and_tables(pdf_path):
    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in tqdm(range(len(pdf.pages)), desc="Processing Pages", unit="page"):
            page = pdf.pages[page_number]

            # Extract text
            text = page.extract_text()
            all_text.append(f"\n--- Page {page_number + 1} ---\n" + (text if text else ""))

    return all_text

all_text = extract_text_and_tables(pdf_path)
all_text

import re
# Regular expression pattern to match "Intake Pallet QC Inspection Report" with a page header
pattern = re.compile(r"^\n--- Page \d+ ---\nIntake Pallet QC Inspection Report", re.MULTILINE)

# Filtering the list
filtered_blocks = [block for block in all_text if pattern.search(block)]
last_block_len = len(filtered_blocks[-1])

# remove last pages with only images
final_items = [block for block in filtered_blocks if len(block)>last_block_len]

print(final_items[0])

import os
import json
import torch
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import sys

# Ensure the parent directory is in the path
sys.path.append('..')
from configs.report_config import get_qc_prompt

# Load 4-bit Quantized Model
print("Loading model and tokenizer...")

model_name = "Qwen/Qwen2.5-14B"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, 
    bnb_4bit_compute_dtype=torch.bfloat16  # Set computation dtype
)

model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    quantization_config=bnb_config,  # Apply quantization during loading
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

print("Model loaded successfully!")

# Create output directory
output_folder = "qc_reports_14b"
os.makedirs(output_folder, exist_ok=True)

# Function to generate JSON output directly from the model
def generate_json_output(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(**inputs)
    
    # Decode and clean up response
    response = tokenizer.decode(outputs[0])
    return response

responses = []
# Process each page
for i, page in enumerate(tqdm(final_items, desc="Processing Pages", unit="page")):
    prompt = get_qc_prompt(page)  # Get structured prompt
    response = generate_json_output(prompt)  # Ask model directly for JSON
    responses.append(response)
    if i > 1:
        break
    # Save JSON output
    # output_path = os.path.join(output_folder, f"qc_report_page_{i}.json")
    # with open(output_path, "w", encoding="utf-8") as json_file:
    #     json.dump(response, json_file, indent=4, ensure_ascii=False)

    # print(f"Saved: {output_path}")


for response in responses:
    print(response[len(prompt):])

def extract_json_objects(text):
    json_pattern = r'\{.*?\}'
    json_matches = re.findall(json_pattern, text, re.DOTALL)  # Find all JSON objects
    json_objects = []
    
    for match in json_matches:
        try:
            json_obj = json.loads(match)  # Convert to dictionary
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            continue  # Ignore invalid JSON
    
    return json_objects

extract_json_objects(responses[0])