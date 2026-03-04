# This file makes the folder a Python package

from logger.custom_logger import CustomLogger

GLOBAL_LOGGER = CustomLogger().get_logger(__file__)
