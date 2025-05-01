

import os
from pathlib import Path

# Set correct package name
package_name = "SmartLegalAssistant"

# Define all necessary files and directories
list_of_files = [
    # CI/CD
    Path(".github") / "workflows" / ".gitkeep",

    # Core src folders
    f"src/__init__.py",
    f"src/{package_name}/__init__.py",

    # Ingestion
    f"src/{package_name}/ingestion/__init__.py",
    f"src/{package_name}/ingestion/downloader.py",
    f"src/{package_name}/ingestion/extractor.py",

    # Processor
    f"src/{package_name}/processor/__init__.py",
    f"src/{package_name}/processor/chunker.py",
    f"src/{package_name}/processor/embedder.py",

    # Vectorstore
    f"src/{package_name}/vectorstore/__init__.py",
    f"src/{package_name}/vectorstore/pineconedb.py",

    # Chat
    f"src/{package_name}/chat/__init__.py",
    f"src/{package_name}/chat/retriever.py",
    f"src/{package_name}/chat/prompt_builder.py",
    f"src/{package_name}/chat/chatagent.py",

    # Pipelines
    f"src/{package_name}/pipelines/__init__.py",
    f"src/{package_name}/pipelines/index_pipeline.py",
    f"src/{package_name}/pipelines/query_pipeline.py",

    # Config and utilities
    f"src/{package_name}/config/__init__.py",
    f"src/{package_name}/config/config.py",
    f"src/{package_name}/utils/__init__.py",
    f"src/{package_name}/utils/file_utils.py",

    # UI (optional frontend)
    f"src/{package_name}/ui/__init__.py",
    f"src/{package_name}/ui/streamlit_app.py",

    # Common modules
    f"src/{package_name}/exception.py",
    f"src/{package_name}/logger.py",

    # Project files
    "experiment.ipynb",
    "streamlit_app.py",
    "streamlit_app.py",
    "requirements.txt",
    "pyproject.toml",
    "Dockerfile",
    "README.md",

    # # Data folders with .gitkeep
    # "data/raw/.gitkeep",
    # "data/processed/.gitkeep",

    # # Tests
    # "tests/__init__.py",
    # "tests/test_downloader.py",
    # "tests/test_chunker.py",
    # "tests/test_retriever.py",
]

# Create directories and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass

print(f"✅ Project structure for `{package_name}` has been generated.")
