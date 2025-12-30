from pathlib import Path

from converters.pdf_to_docx import pdf_to_docx
from converters.pdf_to_images import pdf_to_images
from converters.docx_to_pdf import docx_to_pdf
from converters.images_to_pdf import images_to_pdf
from utils.logger import setup_logger
from file_manager import FileManager

logger = setup_logger("dispatcher")


def dispatch(input_path: str, output_format: str) -> Path:
    logger.info(
        "Solicitação de conversão | arquivo=%s | formato=%s",
        input_path,
        output_format,
    )

    input_file = FileManager.validate_input(input_path)
    output_format = output_format.upper()

    if output_format == "DOCX":
        return pdf_to_docx(input_file)

    if output_format in ("JPEG", "PNG"):
        return pdf_to_images(input_file, output_format.lower())

    if output_format == "PDF_DOCX":
        return docx_to_pdf(input_file)

    if output_format == "PDF_IMAGES":
        return images_to_pdf(input_file)

    logger.error("Formato de conversão não suportado: %s", output_format)
    raise ValueError(f"Formato não suportado: {output_format}")
