from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QComboBox,
    QTextEdit,
    QMessageBox,
    QProgressBar,
)
from PyQt6.QtCore import QThread, pyqtSignal

from converters.dispatcher import dispatch
from utils.logger import setup_logger

logger = setup_logger("ui")


class ConverterWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, file_path: str, output_format: str):
        super().__init__()
        self.file_path = file_path
        self.output_format = output_format

    def run(self):
        try:
            result = dispatch(self.file_path, self.output_format)
            self.finished.emit(str(result))
        except Exception as exc:
            self.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Converter")
        self.resize(520, 420)

        self.file_path: str | None = None

        self._build_ui()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        title = QLabel("Sistema de Conversão de Arquivos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        self.file_label = QLabel("Nenhum arquivo selecionado")
        self.file_label.setStyleSheet("color: #555;")
        main_layout.addWidget(self.file_label)

        btn_select = QPushButton("Selecionar Arquivo")
        btn_select.clicked.connect(self.select_file)
        main_layout.addWidget(btn_select)

        format_layout = QHBoxLayout()
        format_label = QLabel("Formato de saída:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(
            [
                "DOCX",
                "JPEG",
                "PNG",
                "PDF_DOCX",
                "PDF_IMAGES",
            ]
        )

        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        main_layout.addLayout(format_layout)

        self.convert_btn = QPushButton("Converter")
        self.convert_btn.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.convert_btn)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # modo indeterminado
        self.progress.hide()
        main_layout.addWidget(self.progress)

        log_label = QLabel("Status:")
        main_layout.addWidget(log_label)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

        central_widget.setLayout(main_layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar arquivo"
        )
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path)
            self.log_area.append(f"Arquivo selecionado: {file_path}")
            logger.info("Arquivo selecionado: %s", file_path)

    def start_conversion(self):
        if not self.file_path:
            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um arquivo antes de converter.",
            )
            return

        output_format = self.format_combo.currentText()

        self.convert_btn.setEnabled(False)
        self.progress.show()
        self.log_area.append("Iniciando conversão...")

        logger.info(
            "Iniciando conversão | arquivo=%s | formato=%s",
            self.file_path,
            output_format,
        )

        self.worker = ConverterWorker(self.file_path, output_format)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, result_path: str):
        self.progress.hide()
        self.convert_btn.setEnabled(True)

        self.log_area.append(f"Conversão concluída: {result_path}")
        QMessageBox.information(
            self,
            "Sucesso",
            "Conversão realizada com sucesso!",
        )

        logger.info("Conversão concluída: %s", result_path)

    def on_error(self, error_message: str):
        self.progress.hide()
        self.convert_btn.setEnabled(True)

        self.log_area.append(f"Erro: {error_message}")
        QMessageBox.critical(
            self,
            "Erro",
            f"Ocorreu um erro:\n{error_message}",
        )

        logger.error("Erro na conversão: %s", error_message)
