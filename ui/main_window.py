from pathlib import Path
import os

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
    QFrame,
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

from converters.dispatcher import dispatch_conversion
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
            result = dispatch_conversion(self.file_path, self.output_format)
            self.finished.emit(str(result))
        except Exception as exc:
            self.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de Arquivos")
        self.resize(620, 540)

        self.file_path: str | None = None

       
        self.setAcceptDrops(True)

        self._build_ui()
        self._apply_styles()

    

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        file_path = urls[0].toLocalFile()
        if not file_path:
            return

        self.file_path = file_path
        self.file_label.setText(file_path)
        self.log_area.append(f"Arquivo recebido por drag & drop: {file_path}")
        logger.info("Arquivo recebido por drag & drop: %s", file_path)

   

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Conversor de Arquivos")
        title.setObjectName("title")

        subtitle = QLabel(
            "Arraste um arquivo ou selecione manualmente para converter"
        )
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(divider)

       
        file_card = QFrame()
        file_card.setObjectName("card")
        file_layout = QVBoxLayout(file_card)

        file_title = QLabel("Arquivo de entrada")
        file_title.setObjectName("sectionTitle")

        self.file_label = QLabel("Arraste o arquivo aqui")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_select = QPushButton("Selecionar Arquivo")
        btn_select.setObjectName("secondaryButton")
        btn_select.clicked.connect(self.select_file)

        file_layout.addWidget(file_title)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(btn_select)

        main_layout.addWidget(file_card)

        
        config_card = QFrame()
        config_card.setObjectName("card")
        config_layout = QVBoxLayout(config_card)

        config_title = QLabel("Configuração da conversão")
        config_title.setObjectName("sectionTitle")

        format_layout = QHBoxLayout()
        format_label = QLabel("Formato de saída:")

        self.format_combo = QComboBox()
        self.format_combo.addItems(
            ["DOCX", "JPEG", "PNG", "PDF"]
        )

        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)

        self.convert_btn = QPushButton("Converter")
        self.convert_btn.setObjectName("primaryButton")
        self.convert_btn.clicked.connect(self.start_conversion)

        config_layout.addWidget(config_title)
        config_layout.addLayout(format_layout)
        config_layout.addWidget(self.convert_btn)

        main_layout.addWidget(config_card)

        
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        main_layout.addWidget(self.progress)

        
        status_card = QFrame()
        status_card.setObjectName("card")
        status_layout = QVBoxLayout(status_card)

        status_title = QLabel("Status da conversão")
        status_title.setObjectName("sectionTitle")

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.log_area)

        main_layout.addWidget(status_card)

        central.setLayout(main_layout)


    def _apply_styles(self):
        self.setStyleSheet(
            """
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
            }

            QLabel#title {
                font-size: 26px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #666;
                margin-bottom: 14px;
            }

            QLabel#sectionTitle {
                font-weight: bold;
                margin-bottom: 6px;
            }

            QFrame#card {
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 14px;
            }

            QLabel#fileLabel {
                padding: 22px;
                border: 2px dashed #2563eb;
                border-radius: 10px;
                background-color: #ffffff;
                color: #333;
            }

            QPushButton {
                padding: 10px;
                border-radius: 8px;
            }

            QPushButton#primaryButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
            }

            QPushButton#primaryButton:pressed {
                background-color: #1e40af;
            }

            QPushButton#secondaryButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                border: none;
            }

            QPushButton#secondaryButton:pressed {
                background-color: #1e40af;
            }

            QTextEdit {
                border-radius: 8px;
            }
            """
        )


    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar arquivo"
        )
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path)
            self.log_area.append(f"Arquivo selecionado: {file_path}")

    def start_conversion(self):
        if not self.file_path:
            QMessageBox.warning(
                self, "Atenção", "Selecione ou arraste um arquivo."
            )
            return

        
        self.log_area.clear()
        self.log_area.append("Iniciando nova conversão...\n")

        self.convert_btn.setEnabled(False)
        self.progress.show()

        self.worker = ConverterWorker(
            self.file_path, self.format_combo.currentText()
        )
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, result_path: str):
        self.progress.hide()
        self.convert_btn.setEnabled(True)

        output_file = Path(result_path)
        output_dir = output_file.parent

        self.log_area.append(f"Conversão concluída: {output_file}")
        logger.info("Arquivo convertido com sucesso: %s", output_file)

        QMessageBox.information(
            self,
            "Sucesso",
            "Conversão realizada com sucesso!\nA pasta de saída será aberta."
        )

        try:
            os.startfile(str(output_dir))
        except Exception as exc:
            logger.warning(
                "Não foi possível abrir a pasta de saída: %s", exc
            )

    def on_error(self, error_message: str):
        self.progress.hide()
        self.convert_btn.setEnabled(True)
        self.log_area.append(f"Erro: {error_message}")
        QMessageBox.critical(self, "Erro", error_message)
