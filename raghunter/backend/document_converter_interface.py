from abc import ABC, abstractmethod

class DocumentConverterInterface(ABC):
    """Interface for document conversion operations."""

    @abstractmethod
    def convert(self, source: str) -> str:
        """Convert a document to markdown format.

        Args:
            source: The source document path or URL

        Returns:
            str: The converted markdown content
        """
        pass

    @abstractmethod
    def convert_and_save(self, source: str, output_dir: str) -> None:
        """Convert a document and save it to the output directory.

        Args:
            source: The source document path or URL
            output_dir: The output directory path
        """
        pass


class BackendType(enum):
    DOCLING = 'docling'
    MINERU = 'mineru'


class ConverterFactory:
    @staticmethod
    def get_converter(backend_type: BackendType) -> DocumentConverterInterface:
        if backend_type == BackendType.DOCLING:
            return DoclingConverter()
        elif backend_type == BackendType.MINERU:
            return MineruConverter()
        else:
            raise ValueError(f"Unsupported backend type: {backend_type}")