import logging
import os
from datetime import datetime

from config import params


def log_settings():
    dt = datetime.now()
    file_log = logging.FileHandler(os.path.join(params.logs_path, f'{dt.strftime("%Y-%m-%d")}.log'), 'a', 'utf-8')
    console_out = logging.StreamHandler()
    logging.basicConfig(handlers=(file_log, console_out),
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')

    logging.getLogger().setLevel(logging.INFO)
    root_logger = logging.getLogger(__name__)

    return root_logger


logger = log_settings()
