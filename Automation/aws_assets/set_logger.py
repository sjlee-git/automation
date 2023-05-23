import logging
from datetime import datetime

def set_logger(file_path):
    # Set Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log를 파일에 출력
    file_name = 'log_' + datetime.now().strftime('%Y-%m-%d') + '.log'
    file_handler = logging.FileHandler(file_path + '/log/' + file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger