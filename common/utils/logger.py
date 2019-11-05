import logging
import os


def start_logging(client):
    # see numeric represents level here: https://docs.python.org/3/library/logging.html#logging-levels
    logging_mode = os.getenv('COMMON_API_CLIENT_LOGGING_MODE', 10)  # debug by default

    logging.basicConfig(level=logging_mode,
                        filename='app.log',
                        filemode='w',
                        format='[%(asctime)s] - [%(levelname)s] - %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S')

    logging.info('Start logging...')
    logging.info(f'Client {client.__class__.__name__} was created with:'
                 f' host - {client.url},'
                 f' headers - {client.headers}')
