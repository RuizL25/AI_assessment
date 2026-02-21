"""
PDF loading utility.

Provides functions to load PDF files.
"""

from typing import List
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str) -> str:
    """Loads a PDF file and returns its text content.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The text content of the PDF file.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If any other error occurs during PDF loading.
    """
    try:
        loader = PyPDFLoader(file_path)
        # Load documents, which is a list of LangChain Documents
        # We will concatenate their page content to get the full text.
        docs = loader.load()
        full_text = "\n".join([doc.page_content for doc in docs])
        return full_text
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        raise Exception(f"Error loading PDF '{file_path}': {e}")
