from config.settings import SRC_DIR
import os
os.chdir(SRC_DIR)

from document_processing_system.components.data_ingestion import DataIngestion
from document_processing_system.components.data_extraction import DataExtraction

data_ingester = DataIngestion('qc_data/qc_templates/PO 177692 - PO 221421.pdf')
data_extracter = DataExtraction(data_ingester)
pages, tables, images = data_extracter.extract_data()
all_items = data_extracter.filter_pages(pages)

from document_processing_system.components.model_inference import ModelInference
model = ModelInference()
response = model.process_items(all_items)

import pandas as pd
flat_data = [item for sublist in response for item in sublist]

data = pd.DataFrame(flat_data)
print(data)