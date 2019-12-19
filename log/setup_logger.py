import logging, os, pathlib

log_fname = pathlib.Path(os.getcwd(), 'ecommerce_auto_buyer_log.log')

logging.basicConfig(filename=log_fname, level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger('ecommerce_auto_buyer')

