from openvpn.OpenVpn import OpenVpn
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import os

def setup_selenium():
    options = Options()
    options.headless = False
    browser_locale = 'pl'
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', browser_locale)

    browser = webdriver.Firefox(options=options, firefox_profile=profile)
    browser.delete_all_cookies()
    browser.set_window_size(1800, 600)
    browser.set_window_position(0, 0)
    return browser

def find_working_configs(config_name):
    vpn = OpenVpn(config_name)
    already_connected = vpn.check_connection()
    timeout = 0
    while already_connected == True:
        vpn.disconnect()
        already_connected = vpn.check_connection()
        timeout += 10
        if timeout == 10:
            while already_connected == True:
                print('Script can not disconnect from vpn automatically, please do it manually')
                input('Type y if you disconnected manually: ')
                already_connected = vpn.check_connection()
    connected = vpn.connect()
    browser = setup_selenium()
    if connected == True:
        browser.get('https://allegro.pl/')
        delay = 5  # seconds
        try:
            consent_xpath = '//button[@type=\'button\'][@data-role=\'accept-consent\']'
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, consent_xpath)))
            print('config: {} working'.format(config_name))
            browser.close()
        except TimeoutException:
            print('config: {} not working, cant load a page'.format(config_name))
            browser.close()
    else:
        print('config: {} not working, cant connect'.format(config_name))
        browser.close()

config_list = os.listdir('C:\Program Files\OpenVPN\config')
for name in config_list:
    if name != 'login.conf':
        find_working_configs(name)


