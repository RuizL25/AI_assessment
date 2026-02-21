"""
Chunk description module.

This module provides a function to generate descriptions for each chunk
This description is used to generate the vector store.
"""

from typing import List
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from rag.prompts import PROMPT_CHUNK_DESCRIPTION
from rag.multimodal_model import ocr_client

def chunk_description_pipeline(chunks: List[Document])-> List[str]:
    """Generate descriptions for each chunk.

    Args:
        chunks: List of chunks to generate descriptions for.

    Returns:
        List of descriptions for each chunk.
    """

    prompt = PromptTemplate.from_template(PROMPT_CHUNK_DESCRIPTION)

    chain = prompt | ocr_client | StrOutputParser()
    bacht_inputs = [{"chunk_text": chunk.page_content} for chunk in chunks]

    try:
        chunks_description = chain.batch(bacht_inputs, config={"max_concurrency": 5})
    except Exception as e:
        print(f"Error en batch processing: {e}")
        raise e

    return chunks_description
