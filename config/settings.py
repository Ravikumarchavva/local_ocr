from pathlib import Path

# Get the root directory dynamically
ROOT_DIR = Path(__file__).resolve().parent.parent

# Define other key directories
CONFIG_DIR = ROOT_DIR / "config"
DATA_DIR = ROOT_DIR / "data"
SRC_DIR = ROOT_DIR / "src"
TEST_DIR = ROOT_DIR / "test"
DOCS_DIR = ROOT_DIR / "docs"
