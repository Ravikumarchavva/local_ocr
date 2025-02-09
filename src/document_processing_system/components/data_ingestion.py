from config.settings import DATA_DIR
import os
from dataclasses import dataclass

@dataclass
class DataIngestion:
    file_name: str

    def __post_init__(self):
        self.update_file_path(self.file_name)

    def update_file_path(self, new_file_name):
        """Update the file path when the file name is changed."""
        self.file_name = new_file_name
        self.file_path = os.path.join(DATA_DIR, self.file_name)

if __name__ == '__main__':
    data_ingester = DataIngestion('qc_data/qc_templates/PO166939-204865.pdf')
    print("Initial Path:", data_ingester.file_path)

    # Change file path
    data_ingester.update_file_path('DPS9 PO 177768 - 221234 Summary Report.pdf')
    print("Updated Path:", data_ingester.file_path)
