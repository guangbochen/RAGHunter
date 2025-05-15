import os
import json
from .document_converter_interface import DocumentConverterInterface

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

class DoclingConverter(DocumentConverterInterface):
    """Backend class for handling document conversion operations."""

    def __init__(self):
        # self._converter = DocumentConverter()
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True
        pipeline_options.accelerator_options = AcceleratorOptions(
            num_threads=4, device=AcceleratorDevice.AUTO
        )

        self._converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def convert(self, source: str) -> str:
        """Convert a document to markdown format.

        Args:
            source: The source document path or URL

        Returns:
            str: The converted markdown content
        """
        doc = self._converter.convert(source).document
        # return doc.export_to_markdown()
        return doc.export_to_markdown()

    def convert_and_save(self, source: str, output_dir: str) -> None:
        """Convert a document and save it to the output directory.

        Args:
            source: The source document path or URL
            output_dir: The output directory path
        """
        content = self.convert(source)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save the converted document to the output directory with the same name but with .md extension
        # TODO: add support for saving to s3 if the user wants to use s3 as the output destination
        # TODO: add support for saving to a different format if the user wants to use a different format
        # TODO: add support for saving to a different name if the user wants to use a different name
        with open(f"{output_dir}/{os.path.basename(source)}.md", "w", encoding="utf-8") as f:
            f.write(content)