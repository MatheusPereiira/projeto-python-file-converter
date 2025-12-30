from pathlib import Path
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from file_manager import FileManager
from utils.logger import setup_logger

logger = setup_logger("docx_to_pdf")


def docx_to_pdf(input_file: Path) -> Path:
    logger.info("Iniciando conversão DOCX → PDF | arquivo=%s", input_file)

    try:
        output_path = FileManager.build_output_path(input_file, "pdf")

        document = Document(str(input_file))
        pdf = canvas.Canvas(str(output_path), pagesize=A4)

        width, height = A4
        x_margin = 40
        y_position = height - 40
        line_height = 14

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if not text:
                y_position -= line_height
                continue

            if y_position <= 40:
                pdf.showPage()
                y_position = height - 40

            pdf.drawString(x_margin, y_position, text)
            y_position -= line_height

        pdf.save()

        logger.info(
            "Conversão DOCX → PDF finalizada com sucesso | arquivo_saida=%s",
            output_path,
        )

        return output_path

    except Exception as exc:
        logger.error(
            "Erro ao converter DOCX para PDF | arquivo=%s",
            input_file,
            exc_info=True,
        )
        raise exc
