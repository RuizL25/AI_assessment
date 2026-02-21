"""
Service to save a markdown document to a file.
"""

import os

from utils.config import settings

def save_md_doc(md_doc: str, file_name: str) -> str:
    """Saves a markdown document to a file.

    Args:
        md_doc: The markdown document to save.
        file_name: The name of the file to save the document to.

    Returns:
        The path to the saved markdown document.
    """

    output_dir = settings.output_dir + "/" + file_name.split(".")[0]

    base_name = os.path.basename(file_name)
    file_path = os.path.join(output_dir, f"{base_name}_md.md")

    if os.path.exists(file_path):
        os.remove(file_path)
    
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_doc)
    return file_path
