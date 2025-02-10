import re
import json
from document_processing_system.components.gemini_components.report import Report
from document_processing_system.components.gemini_components.invoice import Invoice


class ReportExtractor:
    def __init__(self):
        pass

    def extract(self, response_text):
        '''Extracts JSON data from model response.'''
        # Adjust regex to capture multiple items inside an array
        match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if match:
            try:
                extracted_data = json.loads(match.group(0))
                return Report(extracted_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON structure in response.")
        raise ValueError("No valid JSON found in response")


class InvoiceExtractor:
    def __init__(self):
        pass

    def extract(self, response_text):
        '''Extracts JSON data from model response.'''
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            extracted_data = json.loads(match.group(0))
            return Invoice(extracted_data)
        raise ValueError("No valid JSON found in response")


