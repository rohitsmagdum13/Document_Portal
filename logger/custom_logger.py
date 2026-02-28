import logging
import os
import sys
from datetime import datetime, timezone

import structlog


class CustomLogger:
    _configured = False

    def __init__(self, log_dir="logs", level=logging.INFO):
        self.level = level
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        self.log_file_path = os.path.join(
            self.logs_dir, f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log"
        )
        self._configure_once()

    def _configure_once(self):
        if CustomLogger._configured:
            return

        app_logger = logging.getLogger("document_portal")
        app_logger.setLevel(self.level)
        app_logger.propagate = False

        formatter = logging.Formatter("%(message)s")

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(self.level)
        stdout_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(self.log_file_path, encoding="utf-8")
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)

        app_logger.handlers.clear()
        app_logger.addHandler(stdout_handler)
        app_logger.addHandler(file_handler)

        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        CustomLogger._configured = True

    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)
        return structlog.get_logger("document_portal").bind(logger_name=logger_name)


if __name__ == "__main__":
    app_logger = CustomLogger().get_logger(__file__)
    app_logger.info("User uploaded a file", user_id=123, filename="report.pdf")
    app_logger.error("Failed to process PDF", error="File not found", user_id=123)
