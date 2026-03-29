"""Logging configuration for the trading bot."""

import logging
import logging.handlers
import os
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file paths
API_LOG_FILE = LOGS_DIR / "api_requests.log"
TRADE_LOG_FILE = LOGS_DIR / "trades.log"
ERROR_LOG_FILE = LOGS_DIR / "errors.log"


def setup_logging():
    """Configure logging for the application."""
    
    # Create root logger
    root_logger = logging.getLogger("trading_bot")
    root_logger.setLevel(logging.DEBUG)
    
    # Remove any existing handlers
    root_logger.handlers = []
    
    # Format
    detailed_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ===== API Logger =====
    api_logger = logging.getLogger("trading_bot.api")
    api_logger.setLevel(logging.DEBUG)
    api_handler = logging.handlers.RotatingFileHandler(
        API_LOG_FILE, maxBytes=5*1024*1024, backupCount=5
    )
    api_handler.setFormatter(detailed_format)
    api_logger.addHandler(api_handler)
    
    # Also log API calls to console
    api_console = logging.StreamHandler()
    api_console.setLevel(logging.INFO)
    api_console.setFormatter(simple_format)
    api_logger.addHandler(api_console)
    
    # ===== Trade Logger =====
    trade_logger = logging.getLogger("trading_bot.trade")
    trade_logger.setLevel(logging.DEBUG)
    trade_handler = logging.handlers.RotatingFileHandler(
        TRADE_LOG_FILE, maxBytes=5*1024*1024, backupCount=5
    )
    trade_handler.setFormatter(detailed_format)
    trade_logger.addHandler(trade_handler)
    
    # Also log trades to console
    trade_console = logging.StreamHandler()
    trade_console.setLevel(logging.INFO)
    trade_console.setFormatter(simple_format)
    trade_logger.addHandler(trade_console)
    
    # ===== Error Logger =====
    error_logger = logging.getLogger("trading_bot.error")
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG_FILE, maxBytes=5*1024*1024, backupCount=5
    )
    error_handler.setFormatter(detailed_format)
    error_logger.addHandler(error_handler)
    
    # Also log errors to console
    error_console = logging.StreamHandler()
    error_console.setLevel(logging.ERROR)
    error_console.setFormatter(simple_format)
    error_logger.addHandler(error_console)
    
    return root_logger, api_logger, trade_logger, error_logger


# Initialize loggers on module import
root_logger, api_logger, trade_logger, error_logger = setup_logging()
