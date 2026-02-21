"""
Save Embeddings Service.

Handles the serialization of text-embedding pairs to disk for inspection.
"""
import json
import os
from typing import List, Sequence
from utils.config import settings

def save_embeddings_to_json(
    texts: Sequence[str], 
    embeddings: Sequence[List[float]], 
    file_name: str
) -> str:
    """
    Saves the texts and their corresponding embeddings to a JSON file.
    """
    if len(texts) != len(embeddings):
        raise ValueError(f"Mismatch: {len(texts)} texts vs {len(embeddings)} embeddings")

    data_to_save = [
        {"text_content": text, "embedding_vector": emb}
        for text, emb in zip(texts, embeddings)
    ]

    output_dir = settings.output_dir + "/" + file_name.split(".")[0]

    base_name = os.path.basename(file_name)
    file_path = os.path.join(output_dir, f"{base_name}_embeddings.json")

    if os.path.exists(file_path):
        os.remove(file_path)
    
    try:    
        os.makedirs(output_dir, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            
        return file_path
    except Exception as e:
        raise RuntimeError(f"Error saving embeddings to JSON: {e}") from e