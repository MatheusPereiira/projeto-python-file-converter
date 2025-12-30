from pathlib import Path
from pdf2docx import Converter
from file_manager import FileManager
from utils.logger import setup_logger

logger = setup_logger("pdf_to_docx")


def pdf_to_docx(input_file: Path) -> Path:
    logger.info("Iniciando conversão PDF → DOCX | arquivo=%s", input_file)

    try:
        output_path = FileManager.build_output_path(input_file, "docx")

        converter = Converter(str(input_file))
        converter.convert(str(output_path))
        converter.close()

        logger.info(
            "Conversão finalizada com sucesso | arquivo_saida=%s",
            output_path,
        )

        return output_path

    except Exception as exc:
        logger.error(
            "Erro ao converter PDF para DOCX | arquivo=%s",
            input_file,
            exc_info=True,
        )
        raise exc
