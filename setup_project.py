"""
setup_project.py
-----------------
Run this script to create the entire project folder structure
and placeholder files for the Document Portal project.

Usage:
    uv run python setup_project.py
"""

import os
import json

# ──────────────────────────────────────────────
# 1. Base directory (root of the project)
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ──────────────────────────────────────────────
# 2. Helper functions
# ──────────────────────────────────────────────
def create_folder(path):
    """Create a folder if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)
    print(f"  [FOLDER]  {os.path.relpath(path, BASE_DIR)}")


def create_file(path, content=""):
    """Create a file with optional content. Skips if file already exists."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [FILE]    {os.path.relpath(path, BASE_DIR)}")
    else:
        print(f"  [EXISTS]  {os.path.relpath(path, BASE_DIR)}")


def create_init(folder_path):
    """Create an __init__.py inside the given folder."""
    create_file(
        os.path.join(folder_path, "__init__.py"),
        '# This file makes the folder a Python package\n',
    )


# ──────────────────────────────────────────────
# 3. Define the project structure
# ──────────────────────────────────────────────
def setup_logging_and_exception():
    """Create logging/ and exception/ folders with their modules."""

    # --- logging ---
    logging_dir = os.path.join(BASE_DIR, "logging")
    create_folder(logging_dir)
    create_init(logging_dir)
    create_file(
        os.path.join(logging_dir, "custom_logger.py"),
        '''"""
custom_logger.py
-----------------
Provides a reusable logger for the entire project.
"""

import logging
import sys


def get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    """Return a configured logger with console output."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
''',
    )

    # --- exception ---
    exception_dir = os.path.join(BASE_DIR, "exception")
    create_folder(exception_dir)
    create_init(exception_dir)
    create_file(
        os.path.join(exception_dir, "custom_exception.py"),
        '''"""
custom_exception.py
--------------------
Defines custom exceptions for the Document Portal project.
"""

import sys


class DocumentPortalException(Exception):
    """Base exception for the Document Portal project."""

    def __init__(self, message: str, error_detail: sys = None):
        super().__init__(message)
        self.message = message

        # Capture file name and line number if available
        if error_detail is not None:
            _, _, tb = error_detail.exc_info()
            if tb is not None:
                self.line_number = tb.tb_lineno
                self.file_name = tb.tb_frame.f_code.co_filename
            else:
                self.line_number = None
                self.file_name = None

    def __str__(self):
        if self.file_name and self.line_number:
            return (
                f"Error in [{self.file_name}] at line [{self.line_number}]: "
                f"{self.message}"
            )
        return self.message
''',
    )


def setup_src():
    """Create src/ folder with sub-modules, each containing a .gitkeep."""

    src_dir = os.path.join(BASE_DIR, "src")
    create_folder(src_dir)
    create_init(src_dir)

    # Sub-folders inside src/
    sub_modules = ["doc_compare", "doc_analyzer", "multi_doc_chat", "single_doc_chat"]

    for module in sub_modules:
        module_dir = os.path.join(src_dir, module)
        create_folder(module_dir)
        create_init(module_dir)
        create_file(os.path.join(module_dir, ".gitkeep"), "")


def setup_utils():
    """Create utils/ folder with llm_utils.py."""

    utils_dir = os.path.join(BASE_DIR, "utils")
    create_folder(utils_dir)
    create_init(utils_dir)
    create_file(
        os.path.join(utils_dir, "llm_utils.py"),
        '''"""
llm_utils.py
-------------
Utility functions for working with LLMs (Groq, Google GenAI, etc.).
"""


def get_llm(provider: str = "groq", model: str = None):
    """
    Return an LLM instance based on the provider.
    Extend this function as you add more providers.
    """
    # TODO: Implement LLM provider logic
    pass
''',
    )


def setup_notebook():
    """Create notebook/ folder with an experiments.ipynb file."""

    notebook_dir = os.path.join(BASE_DIR, "notebook")
    create_folder(notebook_dir)

    # Minimal valid Jupyter notebook structure
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Experiments Notebook\\n", "Use this notebook for prototyping and testing."],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": ["# Write your experiment code here\\n"],
                "execution_count": None,
                "outputs": [],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12.0"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    notebook_path = os.path.join(notebook_dir, "experiments.ipynb")
    if not os.path.exists(notebook_path):
        with open(notebook_path, "w", encoding="utf-8") as f:
            json.dump(notebook_content, f, indent=2)
        print(f"  [FILE]    {os.path.relpath(notebook_path, BASE_DIR)}")
    else:
        print(f"  [EXISTS]  {os.path.relpath(notebook_path, BASE_DIR)}")


def setup_config():
    """Create config/ folder with config.yaml."""

    config_dir = os.path.join(BASE_DIR, "config")
    create_folder(config_dir)
    create_file(
        os.path.join(config_dir, "config.yaml"),
        '''# config.yaml
# -----------
# Central configuration for the Document Portal project.

app:
  name: "Document Portal"
  version: "0.1.0"
  debug: true

# Add your LLM, database, and other settings here
''',
    )


def setup_prompt():
    """Create prompt/ folder with prompt_library.py."""

    prompt_dir = os.path.join(BASE_DIR, "prompt")
    create_folder(prompt_dir)
    create_init(prompt_dir)
    create_file(
        os.path.join(prompt_dir, "prompt_library.py"),
        '''"""
prompt_library.py
------------------
Stores reusable prompt templates for the Document Portal project.
"""

# Example prompt template
SUMMARIZE_PROMPT = """
You are a helpful assistant. Summarize the following document concisely:

{document_text}
"""

QA_PROMPT = """
You are a helpful assistant. Answer the question based on the provided context.

Context:
{context}

Question:
{question}

Answer:
"""
''',
    )


def setup_app():
    """Create app.py (FastAPI backend) in the root directory."""

    create_file(
        os.path.join(BASE_DIR, "app.py"),
        '''"""
app.py
-------
FastAPI backend for the Document Portal.
"""

from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(title="Document Portal", version="0.1.0")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Document Portal is running"}


# Run with:  uvicorn app:app --reload
''',
    )


def setup_template():
    """Create template/ folder with index.html."""

    template_dir = os.path.join(BASE_DIR, "template")
    create_folder(template_dir)
    create_file(
        os.path.join(template_dir, "index.html"),
        '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Portal</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Welcome to Document Portal</h1>
    <p>Upload and analyze your documents.</p>
</body>
</html>
''',
    )


def setup_static():
    """Create static/ folder with style.css."""

    static_dir = os.path.join(BASE_DIR, "static")
    create_folder(static_dir)
    create_file(
        os.path.join(static_dir, "style.css"),
        '''/* style.css — basic styling for Document Portal */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    padding: 2rem;
    background-color: #f5f5f5;
}

h1 {
    color: #333;
    margin-bottom: 1rem;
}
''',
    )


def setup_streamlit_ui():
    """Create streamlit_ui.py in the root directory."""

    create_file(
        os.path.join(BASE_DIR, "streamlit_ui.py"),
        '''"""
streamlit_ui.py
----------------
Streamlit frontend for the Document Portal.

Run with:  streamlit run streamlit_ui.py
"""

import streamlit as st

# Page configuration
st.set_page_config(page_title="Document Portal", layout="wide")

st.title("📄 Document Portal")
st.write("Upload and analyze your documents using AI.")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    # TODO: Add document processing logic here
''',
    )


# ──────────────────────────────────────────────
# 4. Main — run all setup functions
# ──────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Document Portal — Project Structure Setup")
    print("=" * 50)
    print()

    print("[1/10] Creating logging/ and exception/ ...")
    setup_logging_and_exception()
    print()

    print("[2/10] Creating src/ with sub-modules ...")
    setup_src()
    print()

    print("[3/10] Creating utils/ ...")
    setup_utils()
    print()

    print("[4/10] Creating notebook/ ...")
    setup_notebook()
    print()

    print("[5/10] Creating config/ ...")
    setup_config()
    print()

    print("[6/10] Creating prompt/ ...")
    setup_prompt()
    print()

    print("[7/10] Creating app.py ...")
    setup_app()
    print()

    print("[8/10] Creating template/ ...")
    setup_template()
    print()

    print("[9/10] Creating static/ ...")
    setup_static()
    print()

    print("[10/10] Creating streamlit_ui.py ...")
    setup_streamlit_ui()
    print()

    print("=" * 50)
    print("  ✅ Project structure created successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
