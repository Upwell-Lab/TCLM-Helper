import logging
from datetime import datetime
import os

if not os.path.exists('Logs'):
    os.mkdir('Logs')

system_logger = logging.getLogger('system_logger')
system_logger.setLevel(logging.INFO)

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

system_file_handler = logging.FileHandler(f"Logs/system{current_datetime}.log")
system_file_handler.setLevel(logging.INFO)

system_stream_handler = logging.StreamHandler()
system_stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
system_file_handler.setFormatter(formatter)
system_stream_handler.setFormatter(formatter)

system_logger.addHandler(system_file_handler)
system_logger.addHandler(system_stream_handler)