import logging, pathlib

main_dir = pathlib.Path().absolute()
log_fname = '{}/log_files/ecommerce_auto_buyer.log'.format(main_dir)

logging.basicConfig(filename=log_fname, level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger('ecommerce_auto_buyer')

