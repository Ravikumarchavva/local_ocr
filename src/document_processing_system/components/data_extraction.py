from tqdm.auto import tqdm
from data_ingestion import DataIngestion

class DataExtraction:
    def __init__(self, data_ingestion):
        self.data_ingestion = data_ingestion

    def extract_data(self):
        import pdfplumber
        with pdfplumber.open(self.data_ingestion.file_path) as pdf:
            pages = []
            tables = []
            images = []
            for page_no, page in enumerate(tqdm(pdf.pages, desc="Extracting pages", unit="pages"), start=1):
                header = f'\n--------Page: {page_no}-----------\n'
                pages.append(header + page.extract_text())
                tables.append(page.extract_tables())
                images.append(page.images)
        return pages, tables, images

    def display_data(self, data):
        for page in data:
            print(page)

if __name__ == '__main__':
    data_ingestion = DataIngestion('qc_data/qc_templates/PO166939-204865.pdf')
    data_extractor = DataExtraction(data_ingestion)
    pages, tables, images = data_extractor.extract_data()
    data_extractor.display_data(pages)