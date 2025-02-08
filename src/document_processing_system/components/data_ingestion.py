from config.settings import DATA_DIR
import os
from dataclasses import dataclass

@dataclass
class DataIngestion:
    file_name: str

    def __post_init__(self):
        self.file_path = os.path.join(DATA_DIR, self.file_name)


if __name__ == '__main__':
    data_ingester = DataIngestion('qc_data/qc_templates/PO166939-204865.pdf')