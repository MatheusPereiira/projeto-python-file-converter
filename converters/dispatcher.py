from converters.pdf_to_docx import pdf_to_docx
from converters.pdf_to_images import pdf_to_images
from converters.docx_to_pdf import docx_to_pdf
from converters.images_to_pdf import images_to_pdf
from converters.image_to_image import image_to_image


def dispatch_conversion(input_path: str, output_format: str) -> str:
    input_path = input_path.lower()

    # PDF → DOCX
    if output_format == "DOCX":
        if not input_path.endswith(".pdf"):
            raise ValueError("Apenas PDF pode ser convertido para DOCX.")
        return pdf_to_docx(input_path)

    # DOCX / IMAGEM → PDF
    if output_format == "PDF":
        if input_path.endswith(".docx"):
            return docx_to_pdf(input_path)
        if input_path.endswith((".jpg", ".jpeg", ".png")):
            return images_to_pdf(input_path)
        raise ValueError("Formato inválido para conversão em PDF.")

    # PDF → IMAGEM OU IMAGEM → IMAGEM
    if output_format in ("PNG", "JPEG"):
        if input_path.endswith(".pdf"):
            return pdf_to_images(input_path, output_format)
        if input_path.endswith((".jpg", ".jpeg", ".png")):
            return image_to_image(input_path, output_format)
        raise ValueError("Formato inválido para conversão em imagem.")

    raise ValueError("Formato de conversão não suportado.")
