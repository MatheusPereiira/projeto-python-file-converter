<p align="center">
  <img src="assets/banner.png" width="100%">
</p>

<h1 align="center">📂 File Converter</h1>

<p align="center">
  <img src="assets/logo.png" width="180">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt">
  <img src="https://img.shields.io/badge/Desktop-App-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

---

## ⚠️ Aviso
**Status do Projeto:** Em desenvolvimento.

Aplicação desktop desenvolvida em **Python + PyQt6** para conversão de arquivos, com foco em **simplicidade, produtividade e organização.**

---

## 🧩 Visão Geral

O **File Converter** é uma aplicação desktop que permite converter arquivos entre diversos formatos de maneira rápida e intuitiva, utilizando uma interface gráfica moderna e amigável.
O sistema suporta **Drag & Drop**, seleção manual de arquivos e organização automática dos arquivos convertidos em uma pasta de saída.

---

## ✅ Funcionalidades

- Conversão entre múltiplos formatos
- Seleção manual de arquivos
- Drag & Drop
- Exibição do tamanho do arquivo selecionado
- Organização automática na pasta output
- Status detalhado da conversão
- Botão para abrir a pasta de saída
- Sistema de logs

---

## 🔄 Formatos Suportados

## 📄 Documentos
- PDF → DOCX  
- DOCX → PDF  

## 🖼️ Imagens
- PNG → JPEG  
- JPEG → PNG  
- Imagens → PDF  
- PDF → Imagens  

---

## 🖼️ Capturas de Tela

### 🏠 Tela Principal
<p align="center">
  <img src="screenshots/home.png" width="85%">
</p>

### 🔄 Conversão em Andamento
<p align="center">
  <img src="screenshots/conversao.png" width="85%">
</p>

### ✅ Conversão Finalizada
<p align="center">
  <img src="screenshots/sucesso.png" width="85%">
</p>

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.11+ |
| Interface Gráfica | PyQt6 |
| Conversão de Arquivos | Pillow, PyPDF, python-docx |
| Arquitetura | MVC |
| Versionamento | Git & GitHub |

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o repositório
```bash
git https://github.com/MatheusPereiira/projeto-python-file-converter.git
cd file_converter
```
## 2️⃣ Crie um ambiente virtual
```bash
python -m venv venv
```

## ▶️ Ativar o ambiente virtual
```bash
Windows:
.\venv\Scripts\activate
```
## Linux/macOS:
```bash
source venv/bin/activate
```
## 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```
## 4️⃣ Execute o programa
```bash
python main.py
```
---

## 📂 Estrutura do Projeto
```bash
file_converter/
├── assets/              # Banner e logo do projeto
├── converters/          # Módulos de conversão
├── logs/                # Logs da aplicação
├── output/              # Arquivos convertidos
├── screenshots/         # Capturas de tela
├── ui/                  # Interface gráfica (PyQt6)
├── utils/               # Utilitários e logger
├── main.py              # Arquivo principal
├── requirements.txt
└── README.md
```
---
## 📄 Licença
Este projeto está sob a **MIT License**, permitindo uso livre para estudo, modificação e distribuição.

---