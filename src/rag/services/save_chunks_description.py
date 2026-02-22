import json
import os
from typing import List
from utils.config import settings

def save_chunks_descriptions(new_chunks: List[str], file_name: str) -> str:
    """Saves the chunks descriptions to a json file, appending if the file exists.

    Args:
        new_chunks: List of NEW chunks descriptions to save.
        file_name: Name of the file to save the chunks descriptions to.

    Returns:
        Path to the saved file.
    """
    output_dir = settings.output_dir + "/" + file_name.split(".")[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    new_chunks_data = [
        {
            "chunk_id": index+1, 
            "description": chunk, 
        } 
        for index, chunk in enumerate(new_chunks)
    ]
    
    base_name = os.path.basename(file_name)
    file_path = os.path.join(output_dir, f"{base_name}_chunks_description.json")

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(new_chunks_data, f, indent=4, ensure_ascii=False)
    
    return file_path