"""
Document segmentation module into chunks.

This module provides a function to apply segmentation based on the 
document structure, using Markdown headers, followed by recursive character splitting.
"""

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


def mixed_structure_chunking(document: str):

        """
        Apply segmentation based on the document structure, using Markdown headers.
        Large sections are further split using a recursive character text splitter.

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

        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=200,
        )

        final_chunks = text_splitter.split_documents(md_chunks)

        return final_chunks
