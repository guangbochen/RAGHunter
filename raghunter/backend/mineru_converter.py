import os

from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze

from .document_converter_interface import DocumentConverterInterface

class MineruConverter(DocumentConverterInterface):
    """Backend class for handling document conversion operations using Mineru."""

    def convert(self, source: str) -> str:
        """Convert a document to markdown format using Mineru.

        Args:
            source: The source document path or URL

        Returns:
            str: The converted markdown content
        """
        pdf_file_name = source
        name_without_suff = pdf_file_name.split(".")[0]

        local_image_dir, local_md_dir = "output/images", "output"
        image_dir = str(os.path.basename(local_image_dir))

        os.makedirs(local_image_dir, exist_ok=True)

        image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_md_dir)

        reader1 = FileBasedDataReader("")
        pdf_bytes = reader1.read(pdf_file_name)

        ds = PymuDocDataset(pdf_bytes)

        if ds.classify() == SupportedPdfParseMethod.OCR:
            ds.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer).dump_md(md_writer, f"{name_without_suff}.md", image_dir)
        else:
            ds.apply(doc_analyze, ocr=False).pipe_txt_mode(image_writer).dump_md(md_writer, f"{name_without_suff}.md", image_dir)

        return f"{local_md_dir}/{name_without_suff}.md"

    def convert_and_save(self, source: str, output_dir: str) -> None:
        """Convert a document and save it to the output directory using Mineru.

        Args:
            source: The source document path or URL
            output_dir: The output directory path
        """
        content = self.convert(source)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f"{output_dir}/{os.path.basename(source)}.md", "w", encoding="utf-8") as f:
            f.write(content)