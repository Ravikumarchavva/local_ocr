from pathlib import Path
ROOT_DIR = Path().resolve().parent.parent

pdf_path = ROOT_DIR / 'data' / 'pure_pdfs' / "PO 166939 - 204865    Summary and Detail Report.pdf"

import fitz
import os
from tqdm.auto import tqdm

# def extract_images_from_pdf(pdf_path, output_folder):
#     doc = fitz.open(pdf_path)
    
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     for page_number in tqdm(range(len(doc)), desc="Extracting images", unit="page"):
#         for img_index, img in enumerate(doc[page_number].get_images(full=True)):
#             try:
#                 xref = img[0]
#                 base_image = doc.extract_image(xref)
#                 image_bytes = base_image["image"]
#                 image_ext = base_image["ext"]

#                 image_filename = f"{output_folder}/page_{page_number+1}_img_{img_index+1}.{image_ext}"
#                 with open(image_filename, "wb") as img_file:
#                     img_file.write(image_bytes)
#             except Exception as e:
#                 print(f"Error extracting image: {e}")

#     print("Extraction complete.")

# extract_images_from_pdf(pdf_path, "extracted_images")

import pdfplumber
import re
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    extracted_data = []

    with pdfplumber.open(pdf_path) as pdf:
        # select the second page
        for page_number, page in enumerate(tqdm(pdf.pages[1:2], desc="Extracting text", unit="page"), start=1):
            text = page.extract_text()
            if text:
                extracted_data.append(f"Page {page_number}:\n{text}\n{'-'*50}")

    return "\n".join(extracted_data)

def extract_key_value_pairs(text):
    # Define expected keys based on the sample output.
    valid_keys = {
        "Product Name", "Status", "ExpectedQty", "ReceivedQty",
        "Supplier Code", "Supplier", "COO", "Vehicle No", "Received", 
        "Vessel", "Inspection Date", "Print date", "ISS Pallet ID", "Freshness Technology",
        "Supplier Pallet ID", "Punnet / Pad Type", "Customer Pallet ID", "Outer", 
        "Variety", "Brand", "Grower", "Organic?", "Does Pallet Meet Spec?",
        "GGN", "PLU?", "Orchard/Farm", "End Customer", "Harvest Date", "DP",
        "Total Defects", "Size/Calibre", "Packhouse", "Lot Number", "Inspector",
        "Estimated Yield", "Minor", "Major", "Defects Tot", "Defects Fruit Total",
        "Packs With Defects", "Waste Tot", "Waste Fruit Total", "Packs With Waste",
        "Minor Defects Tot", "Minor Fruit Total", "Major Defects Tot", "Major Fruit Total",
        "Packs With Major", "Box / Pack Weights", "Weight Readings", "Fruit Weights",
        "Sugar Brix", "Brix Readings", "Size", "Size Readings", "Maturity %",
        "Pressures", "Other Issues", "QA Comments", 
        "Packs/Fruits Inspected/Sample Size", "Boxes Inspected", "C"
    }
    pattern = r"(?P<key>[a-zA-Z\ %\/?]+?)\s*[:—\-](?!\d)(?P<value>.*?)(?=\s{4,}(?!\d)|:\s*:\s*|\n|$)"
    matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
    result = {}
    prev_key = None
    for match in matches:
        key = match.group("key").strip()
        value = match.group("value").strip()
        # If no value is found, set it as None
        if value == "":
            value = None
        if key in valid_keys:
            if key in result:
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
            prev_key = key
        else:
            # If not a valid key, append its content to the previous key value.
            if prev_key:
                additional = f"{key} : {value}" if value is not None else f"{key} : None"
                if isinstance(result[prev_key], list):
                    result[prev_key][-1] = (result[prev_key][-1] or "") + " " + additional
                else:
                    result[prev_key] = (result[prev_key] or "") + " " + additional
    return result

text = extract_text_from_pdf(pdf_path)
extracted_pairs = extract_key_value_pairs(text)
for key, value in extracted_pairs.items():
    print(f"Key: {key}, Value: {value}")


