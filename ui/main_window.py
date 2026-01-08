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
        self.resize(620, 560)

        self.file_path: str | None = None
        self.last_output_dir: Path | None = None

        self.setAcceptDrops(True)

        self._build_ui()

    # =========================
    # UTIL
    # =========================
    def _format_file_size(self, file_path: str) -> str:
        size = os.path.getsize(file_path)

        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"

    # =========================
    # DRAG & DROP
    # =========================
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

        self._set_selected_file(file_path)
        self.log_area.append(f"Arquivo recebido por drag & drop: {file_path}")

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(16)

        title = QLabel("Conversor de Arquivos")
        title.setStyleSheet("font-size:26px;font-weight:bold;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Arraste um arquivo ou selecione manualmente para converter"
        )
        layout.addWidget(subtitle)

        layout.addWidget(QFrame(frameShape=QFrame.Shape.HLine))

        # -------- Arquivo --------
        file_box = QFrame()
        file_box.setFrameShape(QFrame.Shape.StyledPanel)
        file_layout = QVBoxLayout(file_box)

        file_title = QLabel("Arquivo de entrada")
        file_title.setStyleSheet("font-weight:bold;")

        self.file_label = QLabel("Arraste o arquivo aqui")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet(
            "border:2px dashed #2563eb;"
            "padding:20px;"
            "border-radius:8px;"
        )

        btn_select = QPushButton("Selecionar Arquivo")
        btn_select.clicked.connect(self.select_file)
        btn_select.setStyleSheet(
            "background:#2563eb;color:white;padding:10px;border-radius:8px;"
        )

        file_layout.addWidget(file_title)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(btn_select)

        layout.addWidget(file_box)

        # -------- Configuração --------
        config_box = QFrame()
        config_layout = QVBoxLayout(config_box)

        config_title = QLabel("Configuração da conversão")
        config_title.setStyleSheet("font-weight:bold;")

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Formato de saída:"))

        self.format_combo = QComboBox()
        self.format_combo.addItems(["DOCX", "PDF", "PNG", "JPEG"])
        format_layout.addWidget(self.format_combo)

        self.convert_btn = QPushButton("Converter")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setStyleSheet(
            "background:#2563eb;color:white;padding:10px;border-radius:8px;"
        )

        self.open_output_btn = QPushButton("Abrir pasta de saída")
        self.open_output_btn.clicked.connect(self.open_output_folder)
        self.open_output_btn.setStyleSheet(
            "background:#2563eb;color:white;padding:10px;border-radius:8px;"
        )

        config_layout.addWidget(config_title)
        config_layout.addLayout(format_layout)
        config_layout.addWidget(self.convert_btn)
        config_layout.addWidget(self.open_output_btn)

        layout.addWidget(config_box)

        # -------- Status --------
        status_box = QFrame()
        status_layout = QVBoxLayout(status_box)

        status_title = QLabel("Status da conversão")
        status_title.setStyleSheet("font-weight:bold;")

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.log_area)

        layout.addWidget(status_box)

        # -------- Progresso --------
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)

    # =========================
    # AÇÕES
    # =========================
    def _set_selected_file(self, file_path: str):
        self.file_path = file_path
        size = self._format_file_size(file_path)
        name = Path(file_path).name

        self.file_label.setText(f"{name} ({size})")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo")
        if file_path:
            self._set_selected_file(file_path)
            self.log_area.append(f"Arquivo selecionado: {file_path}")

    def start_conversion(self):
        if not self.file_path:
            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione ou arraste um arquivo."
            )
            return

        self.log_area.clear()
        self.log_area.append("Iniciando nova conversão...\n")

        self.progress.show()
        self.convert_btn.setEnabled(False)

        self.worker = ConverterWorker(
            self.file_path,
            self.format_combo.currentText()
        )
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, result_path: str):
        self.progress.hide()
        self.convert_btn.setEnabled(True)

        output_file = Path(result_path)
        self.last_output_dir = output_file.parent

        self.log_area.append(f"Conversão concluída: {output_file}")
        logger.info("Arquivo convertido com sucesso: %s", output_file)

        QMessageBox.information(
            self,
            "Sucesso",
            "Conversão realizada com sucesso!"
        )

    def open_output_folder(self):
        if not self.last_output_dir:
            QMessageBox.information(
                self,
                "Aviso",
                "Nenhuma conversão foi realizada ainda."
            )
            return

        if not self.last_output_dir.exists():
            QMessageBox.warning(
                self,
                "Erro",
                "A pasta de saída não foi encontrada."
            )
            return

        os.startfile(str(self.last_output_dir))

    def on_error(self, error_message: str):
        self.progress.hide()
        self.convert_btn.setEnabled(True)
        self.log_area.append(f"Erro: {error_message}")
        QMessageBox.critical(self, "Erro", error_message)
