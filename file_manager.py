from pathlib import Path


class FileManager:
    OUTPUT_DIR = Path("output")
    @staticmethod
    def validate_input(file_path: str) -> Path:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Arquivo não encontrado.")

        if not path.is_file():
            raise ValueError("O caminho informado não é um arquivo.")

        return path

    @classmethod
    def ensure_output_dir(cls) -> Path:
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        return cls.OUTPUT_DIR

    @staticmethod
    def build_output_path(
        input_file: Path, new_extension: str
    ) -> Path:
        output_dir = FileManager.ensure_output_dir()
        return output_dir / f"{input_file.stem}.{new_extension}"
