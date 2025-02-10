import google.generativeai as genai
import os
from IPython.display import display, HTML
from json2html import json2html

from dotenv import load_dotenv
load_dotenv()
GCP_KEY = os.getenv("GCP_KEY")

from config.gemini.dps_qc_report import REPORT_PROMPT, MODEL, MODEL_CONFIG
from document_processing_system.components.gemini_components.extractor import InvoiceExtractor, ReportExtractor

class OCR_Model:
    def __init__(self, model=MODEL):
        genai.configure(api_key=GCP_KEY)
        self.model = genai.GenerativeModel(model)
        genai.GenerationConfig(MODEL_CONFIG)

    def _predict(self, data):
        '''Generates response using the model.'''
        response = self.model.generate_content(
            [{"mime_type": "application/pdf", "data": data}, REPORT_PROMPT],
        )
        return response.text

    def extract(self, data):
        '''Extracts invoice data from the response.'''
        response_text = self._predict(data)
        extractor = ReportExtractor()
        return extractor.extract(response_text)

    def display(self, document, html=False):
        '''Displays the extracted document data.'''
        if html:
            html_table = json2html.convert(json=document.data)
            display(HTML(html_table))
        else:
            display(document.data)