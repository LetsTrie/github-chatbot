import logging

def setup_logger(environment):
    if environment == 'dev':
        logging.basicConfig(
            level=logging.ERROR, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    else:
        logging.basicConfig(
            level=logging.ERROR, 
            format='%(message)s' 
        )
