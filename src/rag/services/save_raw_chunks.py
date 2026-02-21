import json
import os
from typing import List
from langchain_core.documents import Document
from utils.config import settings

def save_chunks(new_chunks: List[Document], file_name: str) -> str:
    """Saves the chunks to a json file, appending if the file exists.

    Args:
        new_chunks: List of NEW chunks to save.
        file_name: Name of the file to save the chunks to.

    Returns:
        Path to the saved file.
    """
    output_dir = settings.output_dir + "/" + file_name.split(".")[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    new_chunks_data = [
        {
            "chunk_id": index+1, 
            "page_content": chunk.page_content, 
            "metadata": chunk.metadata
        } 
        for index, chunk in enumerate(new_chunks)
    ]
    
    base_name = os.path.basename(file_name)
    file_path = os.path.join(output_dir, f"{base_name}_chunks.json")

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_chunks_data, f, indent=4, ensure_ascii=False)
    
    return file_path