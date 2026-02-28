"""Simple class-based exception handling utility powered only by Loguru."""

import os
import traceback

from loguru import logger


class ExceptionHandler:
    _is_configured = False

    def __init__(self, log_dir="logs", level="ERROR"):
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        self.log_file_path = os.path.join(self.logs_dir, "exceptions.log")
        self.level = level

        print(f"[ExceptionHandler] Log directory ready: {self.logs_dir}")
        print(f"[ExceptionHandler] Exception log file: {self.log_file_path}")

        if not ExceptionHandler._is_configured:
            self._configure_logger()

    def _configure_logger(self):
        # Remove only the default stderr handler (id=0), not ALL loguru handlers
        try:
            logger.remove(0)
        except ValueError:
            pass  # Already removed by another module
        logger.add(
            self.log_file_path,
            level=self.level,
            encoding="utf-8",
            enqueue=True,
            backtrace=False,
            diagnose=False,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[source]} | {message}",
            filter=lambda record: record["extra"].get("source") == "exception_handler",
        )
        logger.add(
            lambda message: print(message, end=""),
            level=self.level,
            format="{time:HH:mm:ss} | {level} | {extra[source]} | {message}",
            filter=lambda record: record["extra"].get("source") == "exception_handler",
        )
        ExceptionHandler._is_configured = True
        print("[ExceptionHandler] Loguru configured successfully.")

    def create_exception(self, message: str, error: Exception | None = None):
        print("[ExceptionHandler] Creating DocumentPortalException.")
        return DocumentPortalException(message=message, original_error=error)

    def log_exception(self, exception: Exception):
        print("[ExceptionHandler] Logging exception.")
        logger.bind(source="exception_handler").error(str(exception))

    def handle_exception(self, message: str, error: Exception) -> None:
        """Create, log, and raise a DocumentPortalException in one call.
        Use this anywhere in the project to handle exceptions consistently.
        """
        app_exception = self.create_exception(message, error=error)
        self.log_exception(app_exception)
        raise app_exception


class DocumentPortalException(Exception):
    def __init__(self, message: str, original_error: Exception | None = None):
        self.message = message
        self.original_error = original_error
        self.file_name = None
        self.line_number = None

        if original_error is not None and original_error.__traceback__ is not None:
            last_frame = traceback.extract_tb(original_error.__traceback__)[-1]
            self.file_name = last_frame.filename
            self.line_number = last_frame.lineno

        super().__init__(self.__str__())

    def __str__(self):
        if self.file_name and self.line_number:
            return f"Error in [{self.file_name}] at line [{self.line_number}]: {self.message}"
        return self.message


if __name__ == "__main__":
    handler = ExceptionHandler()

    try:
        value = int("abc")
        print(value)
    except Exception as error:
        app_exception = handler.create_exception("Failed to convert value to integer.", error=error)
        handler.log_exception(app_exception)
