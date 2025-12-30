from pathlib import Path
import fitz  
from file_manager import FileManager
from utils.logger import setup_logger

logger = setup_logger("pdf_to_images")


def pdf_to_images(input_file: Path, image_format: str) -> Path:
    logger.info(
        "Iniciando conversão PDF → %s | arquivo=%s",
        image_format.upper(),
        input_file,
    )

    if image_format not in ("jpeg", "png"):
        raise ValueError("Formato de imagem não suportado.")

    try:
        output_dir = FileManager.ensure_output_dir()
        pdf = fitz.open(str(input_file))

        for page_index in range(len(pdf)):
            page = pdf.load_page(page_index)
            pix = page.get_pixmap()
            output_file = output_dir / f"{input_file.stem}_page_{page_index + 1}.{image_format}"
            pix.save(str(output_file))

            logger.info(
                "Página convertida | pagina=%s | arquivo=%s",
                page_index + 1,
                output_file,
            )

        pdf.close()

        logger.info(
            "Conversão PDF → imagens finalizada | total_paginas=%s",
            len(pdf),
        )

        return output_dir

    except Exception as exc:
        logger.error(
            "Erro ao converter PDF para imagens | arquivo=%s",
            input_file,
            exc_info=True,
        )
        raise exc
