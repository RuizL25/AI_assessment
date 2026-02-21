"""
Document segmentation module into chunks.

This module provides a function to apply segmentation based on the 
document structure, using Markdown headers.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter


def markdown_structure_chunking(document: str):

        """
        Apply segmentation based on the document structure, using Markdown headers.

        Args:
                document (str): Document to process.

        Returns:
                list: List of chunks generated from the Markdown file.
        """

        markdown_splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")],
                strip_headers=False
        )

        md_chunks = markdown_splitter.split_text(document)

        return md_chunks
