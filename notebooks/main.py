from config.settings import SRC_DIR
import os
os.chdir(SRC_DIR)

from document_processing_system.components.data_ingestion import DataIngestion
from document_processing_system.components.data_extraction import DataExtraction

pdf = 'PO166939-204865'

data_ingester = DataIngestion(f'qc_data/qc_templates/{pdf}.pdf')
data_extracter = DataExtraction(data_ingester)
pages, tables, images = data_extracter.extract_data()
all_items = data_extracter.filter_pages(pages)

import os
from document_processing_system.components.model_inference import ModelInference
from config.settings import DATA_DIR

# Define the PDF folder path
pdf_folder = os.path.join(DATA_DIR, 'qc_data', 'qc_reports_output', pdf, 'qc_reports_14b')

# Ensure the directory exists
os.makedirs(pdf_folder, exist_ok=True)

# Initialize the model
model = ModelInference(model_name="Qwen/Qwen2.5-14B")

response = model.process_items(all_items, output_folder=pdf_folder)

import polars as pl
flat_data = [item for sublist in response for item in sublist]

data = pl.DataFrame(flat_data)

output_folder = os.path.join(DATA_DIR, 'qc_data', 'qc_reports_output', pdf, 'pdf_data')


data.write_excel(f"{output_folder}/data.xlsx")

import json

with open(f'{output_folder}/output.json', "w", encoding="utf-8") as json_file:
    json.dump(flat_data, json_file, indent=4, ensure_ascii=False)
