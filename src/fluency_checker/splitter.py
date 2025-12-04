from typing import Protocol, List
from langchain_text_splitters import MarkdownHeaderTextSplitter

class MarkdownSplitter(Protocol):
    """Protocol for splitting markdown text into segments."""
    
    def split_text(self, text: str) -> List[str]:
        ...



class StringMarkdownHeaderTextSplitter(MarkdownHeaderTextSplitter):
    def split_text(self, text: str) -> List[str]:
        # Get original documents with headers preserved
        documents = super().split_text(text)
        
        # Reconstruct: header + content for each chunk
        result = []
        for doc in documents:
            content = doc.page_content.strip()
            
            # Check if metadata has headers (skip next() - safe check)
            if doc.metadata:
                # Get first available header from metadata
                header_key = next(iter(doc.metadata.keys()), None)
                if header_key:
                    header_value = doc.metadata[header_key]
                    full_chunk = f"{header_key} {header_value}\n\n{content}"
                    result.append(full_chunk)
                    continue
            
            # No headers - just return content (first document case)
            result.append(content)
        
        return result