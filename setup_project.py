"""Create the Document Portal project structure without placeholder content."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def ensure_dir(path: Path) -> None:
    """Create directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def ensure_file(path: Path) -> None:
    """Create empty file if it does not exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def create_python_package(path: Path) -> None:
    """Create package folder with __init__.py."""
    ensure_dir(path)
    ensure_file(path / "__init__.py")


def setup_logging_and_exception() -> None:
    create_python_package(BASE_DIR / "logger")
    ensure_file(BASE_DIR / "logger" / "custom_logger.py")

    create_python_package(BASE_DIR / "exception")
    ensure_file(BASE_DIR / "exception" / "custom_exception.py")

def setup_models() -> None:
    create_python_package(BASE_DIR / "model")
    ensure_dir(BASE_DIR / "model" / "model.py")

def setup_models() -> None:
    create_python_package(BASE_DIR / "model")
    ensure_dir(BASE_DIR / "model" / "model.py")

def setup_src() -> None:
    src_dir = BASE_DIR / "src"
    create_python_package(src_dir)

    create_python_package(src_dir / "document_analyzer")
    ensure_file(src_dir / "document_analyzer" / "data_analysis.py")

    create_python_package(src_dir / "document_chat")
    ensure_file(src_dir / "document_chat" / "retrieval.py")

    create_python_package(src_dir / "document_compare")
    ensure_file(src_dir / "document_compare" / "document_comparator.py")

    create_python_package(src_dir / "document_ingestion")
    ensure_file(src_dir / "document_ingestion" / "data_ingestion.py")


def setup_utils() -> None:
    create_python_package(BASE_DIR / "utils")
    ensure_file(BASE_DIR / "utils" / "llm_utils.py" / "config_loader.py" / "model_loader.py")


def setup_notebook() -> None:
    ensure_dir(BASE_DIR / "notebook")
    ensure_file(BASE_DIR / "notebook" / "experiements.ipynb")


def setup_config() -> None:
    ensure_dir(BASE_DIR / "config")
    ensure_file(BASE_DIR / "config" / "config.yaml")


def setup_prompt() -> None:
    create_python_package(BASE_DIR / "prompt")
    ensure_file(BASE_DIR / "prompt" / "prompt_libraray.py")


def setup_app_files() -> None:
    ensure_file(BASE_DIR / "app.py")
    ensure_file(BASE_DIR / "streamlit_ui.py")


def setup_template_and_static() -> None:
    ensure_dir(BASE_DIR / "template")
    ensure_file(BASE_DIR / "template" / "index.html")

    ensure_dir(BASE_DIR / "static")
    ensure_file(BASE_DIR / "static" / "style.css")


def main() -> None:
    setup_logging_and_exception()
    setup_models()
    setup_src()
    setup_utils()
    setup_notebook()
    setup_config()
    setup_prompt()
    setup_app_files()
    setup_template_and_static()
    print("Project structure is ready.")


if __name__ == "__main__":
    main()
