from tqdm.auto import tqdm
from document_processing_system.components.data_ingestion import DataIngestion
import re
class DataExtraction:
    def __init__(self, data_ingester):
        self.data_ingester = data_ingester

    def extract_data(self):
        import pdfplumber
        with pdfplumber.open(self.data_ingester.file_path) as pdf:
            pages = []
            tables = []
            images = []
            for page_no, page in enumerate(tqdm(pdf.pages, desc="Extracting pages", unit="pages"), start=1):
                header = f'\n--------Page: {page_no}-----------\n'
                pages.append(header + page.extract_text())
                tables.append(page.extract_tables())
                images.append(page.images)
        return pages, tables, images

    @staticmethod
    def display_data(data):
        for page in data:
            print(page)

    @staticmethod
    def filter_pages(pages):
        filtered_pages = []
        for page in tqdm(pages, desc="Filtering pages", unit="pages"):
            items = re.search(r'Expected Qty', page, re.DOTALL)
            if items:
                filtered_pages.append(page)
        return filtered_pages

if __name__ == '__main__':
    data_ingester = DataIngestion('qc_data/qc_templates/PO166939-204865.pdf')
    data_extractor = DataExtraction(data_ingester)
    pages, tables, images = data_extractor.extract_data()
    data_extractor.display_data(pages)