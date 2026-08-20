import logging 
import os 


os.makedirs('logs', exist_ok=True)


error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)

error_formatter = logging.Formatter(
    style='{',
    fmt='[{asctime}] {levelname}: {message}',
    datefmt='%Y-%m-%d %H:%M:%S'
)

error_handler = logging.FileHandler('logs/errors.log', mode='w', encoding='utf-8')  # тут перезапись логичнее 

error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)
error_logger.propagate = False


info_logger = logging.getLogger('info')
info_logger.setLevel(logging.INFO)

info_formatter = logging.Formatter(
    style='{',
    fmt='[{asctime}] {levelname}: {message}',
    datefmt='%Y-%m-%d %H:%M:%S'
)

info_handler = logging.FileHandler('logs/info.log', mode='w', encoding='utf-8')

info_handler.setFormatter(info_formatter)
info_logger.addHandler(info_handler)
info_logger.propagate = False