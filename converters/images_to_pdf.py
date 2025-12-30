from pathlib import Path
from PIL import Image
from file_manager import FileManager
from utils.logger import setup_logger

logger = setup_logger("images_to_pdf")


def images_to_pdf(input_path: Path) -> Path:
   
    logger.info("Iniciando conversão IMAGENS → PDF | caminho=%s", input_path)

    try:
        output_path = FileManager.build_output_path(
            input_path if input_path.is_file() else Path("images"),
            "pdf",
        )

        images = []

        if input_path.is_dir():
            image_files = sorted(
                [
                    p for p in input_path.iterdir()
                    if p.suffix.lower() in (".jpg", ".jpeg", ".png")
                ]
            )
        else:
            image_files = [input_path]

        if not image_files:
            raise ValueError("Nenhuma imagem válida encontrada.")

        for img_path in image_files:
            img = Image.open(img_path).convert("RGB")
            images.append(img)
            logger.info("Imagem adicionada ao PDF | arquivo=%s", img_path)

        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
        )

        logger.info(
            "Conversão IMAGENS → PDF finalizada com sucesso | arquivo_saida=%s",
            output_path,
        )

        return output_path

    except Exception as exc:
        logger.error(
            "Erro ao converter imagens para PDF | caminho=%s",
            input_path,
            exc_info=True,
        )
        raise exc
