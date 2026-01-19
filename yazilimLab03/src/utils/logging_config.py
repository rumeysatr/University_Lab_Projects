"""
Logging yapılandırması modülü
Tüm uygulama genelinde kullanılacak merkezi logging sistemi.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Log seviyesini environment variables'dan oku
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FILE = os.getenv('LOG_FILE', 'logs/application.log')


class ColoredFormatter(logging.Formatter):
    """Renkli konsol çıktısı için formatter"""

    # ANSI renk kodları
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        # Seviyeye göre renk seç
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        # Formatla
        result = super().format(record)
        
        # Orijinal levelname'i geri yükle
        record.levelname = levelname
        return result


def setup_logging(
    level: str = LOG_LEVEL,
    log_file: str = LOG_FILE,
    console_output: bool = True,
    file_output: bool = True
) -> logging.Logger:
    """
    Logging sistemini yapılandırır.

    Args:
        level: Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log dosyası yolu
        console_output: Konsola çıktı ver
        file_output: Dosyaya çıktı ver

    Returns:
        Logger instance
    """
    # Root logger'ı yapılandır
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level, logging.INFO))

    # Mevcut handler'ları temizle
    root_logger.handlers.clear()
    
    # Harici kütüphanelerin logger'larını sakinleştir
    logging.getLogger('openpyxl').setLevel(logging.ERROR)
    logging.getLogger('openpyxl.utils.indexed_list').setLevel(logging.ERROR)
    logging.getLogger('zipfile').setLevel(logging.ERROR)
    logging.getLogger('pandas').setLevel(logging.WARNING)
    logging.getLogger('xlrd').setLevel(logging.ERROR)

    # Formatter oluştur
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    console_formatter = ColoredFormatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Konsol handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    # Dosya handler
    if file_output:
        # Log dizinini oluştur
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Rotating file handler (max 10MB, 5 backup)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level, logging.INFO))
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)

        # Hatalar için ayrı bir dosya
        error_log_file = log_file.replace('.log', '_error.log')
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Belirli bir modül için logger döndürür.

    Args:
        name: Modül adı (genellikle __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Uygulama başlangıcında logging'i yapılandır
_setup_done = False


def init_logging():
    """Logging sistemini ilk başlatma için kullanılır."""
    global _setup_done
    if not _setup_done:
        setup_logging()
        _setup_done = True
