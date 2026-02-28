"""
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
