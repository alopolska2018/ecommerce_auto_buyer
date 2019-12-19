from api_allegro.ModifyBuyNowPrice import ModifyBuyNowPrice
from AllegroAutoBuyer import AllegroAutoBuyer
from api_allegro.GetAllFieldsOfTheParticularOffer import GetAllFieldsOfTheParticularOffer
from openvpn.OpenVpn import OpenVpn
from log.setup_logger import logger
from time import sleep
import keyring
import json


def read_file(filename):
    file = open(filename, 'r')

    auction_numbers = []

    for line in file:
        line = line.strip()
        auction_numbers.append(line)

    return auction_numbers

def read_json_file(filename):
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
        return json_data

def get_accounts_list(json_data):
    accounts_list = []
    for key, val in json_data.items():
        accounts_list.append(key)

    return accounts_list

def get_account_login(accounts_list, n):
    login = accounts_list[n]
    return login

def get_account_password(login):
    password = keyring.get_password('allegro', login)
    return password

def decrease_by_percentage(number, percentage):
    result = number - (float(number)/100 * float(percentage))
    return result

def modify_price(auction_number, login, password):
    allegro_price_checker = GetAllFieldsOfTheParticularOffer()
    allegro_price_modifier = ModifyBuyNowPrice()
    percentage_decrease = input('What percentage do you want to decrease price by:  ')
    account_name = input('Provide allegro account name you are going to buy from: ')
    percentage_decrease = float(percentage_decrease)
    auto_buyer = AllegroAutoBuyer(login, password)

    msg = 'Chosen account: {}'.format(account_name)
    print(msg)
    logger.info(msg)
    original_price = float(allegro_price_checker.get_offer_price(auction_number, account_name))
    msg = 'Orginal price: {}'.format(original_price)
    print(msg)
    logger.info(msg)
    modified_price = int(decrease_by_percentage(original_price, percentage_decrease))
    msg = 'Modified price: {}'.format(modified_price)
    print(msg)
    logger.info(msg)
    allegro_price_modifier.modify_price(auction_number, modified_price, account_name)
    msg = 'price has been modified'
    print(msg)
    logger.info(msg)
    current_price = float(allegro_price_checker.get_offer_price(auction_number, account_name))
    while current_price != modified_price:
        sleep(120)
        msg = 'current_price: {} is not equal modified price: {}'.format(current_price, modified_price)
        print(msg)
        logger.error(msg)
        current_price = float(allegro_price_checker.get_offer_price(auction_number, account_name))
    msg = 'current price {}'.format(current_price)
    print(msg)
    logger.info(msg)

    auto_buyer.perform(auction_number)

    allegro_price_modifier.increase_price(original_price, auction_number, account_name)
    current_price = float(allegro_price_checker.get_offer_price(auction_number, account_name))
    while current_price != original_price:
        msg = 'current_price: {} is not equal original price: {}. Change price manually'.format(current_price,
                                                                                                original_price)
        print(msg)
        logger.error(msg)
        input('Price changed? [type y to continue]')
        current_price = allegro_price_checker.get_offer_price(auction_number, account_name)
    msg = 'original price restored, current price: {}'.format(current_price)
    print(msg)
    logger.info(msg)

def get_config_name(login, json_accounts):
    return json_accounts[login]

def change_ip(login, json_accounts):
    config_name = get_config_name(login, json_accounts)
    vpn = OpenVpn(config_name)
    already_connected = vpn.check_connection()
    #TODO after few tries return error
    timeout = 0
    while already_connected == True:
        vpn.disconnect()
        already_connected = vpn.check_connection()
        timeout += 10
        if timeout == 10:
            while already_connected == True:
                msg = 'Script can not disconnect from vpn automatically, please do it manually'
                print(msg)
                logger.error(msg)
                input('Type y if you disconnected manually: ')
                already_connected = vpn.check_connection()

    vpn.connect()
    already_connected = vpn.check_connection()

    while already_connected == False:
        msg = 'Script can not connect to vpn automatically, please do it manually'
        print(msg)
        logger.error(msg)
        input('Type y if you disconnected manually: ')
        already_connected = vpn.check_connection()

def run():
    filename = input('Enter filename [{file must be inside script dir} ex. auctions.txt]: ')
    logger.info('Chosen file {}'.format(filename))
    choice = input('Modify price of auctions? [y/n]: ')
    logger.info('Modified price option= {}'.format(choice))
    n = 0
    json_accounts = read_json_file('accounts.json')
    accounts_list = get_accounts_list(json_accounts)

    if choice == 'y':
        auction_numbers = read_file(filename)
        for auction_number in auction_numbers:
            if n == len(accounts_list):
                n = 0
            login = get_account_login(accounts_list, n)
            password = get_account_password(login)
            change_ip(login, json_accounts)

            n += 1
            msg = 'Auction number: {}'.format(auction_number)
            print(msg)
            logger.info(msg)
            msg = 'User buying: {}'.format(login)
            print(msg)
            logger.info(msg)
            modify_price(auction_number, login, password)

    elif choice == 'n':
        auction_numbers = read_file(filename)
        for auction_number in auction_numbers:
            if n == len(accounts_list):
                n = 0
            login = get_account_login(accounts_list, n)
            password = get_account_password(login)
            change_ip(login, json_accounts)
            auto_buyer = AllegroAutoBuyer(login, password)
            n += 1
            msg = 'Auction number: {}'.format(auction_number)
            print(msg)
            logger.info(msg)
            msg = 'User buying: {}'.format(login)
            print(msg)
            logger.info(msg)
            auto_buyer.perform(auction_number)
    else:
        print('Wrong choice')

if __name__ == "__main__":
    run()

