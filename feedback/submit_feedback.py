from AllegroAutoBuyer import AllegroAutoBuyer
from openvpn.OpenVpn import OpenVpn
import keyring
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date
import datetime
import re, json
from pathlib import Path
import pickle

class Submit_Feedback():
    def __init__(self):
        self.perform()

    def get_config_name(self, login, json_accounts):
        return json_accounts[login]

    def change_ip(self, config_name):
        vpn = OpenVpn(config_name)
        already_connected = vpn.check_connection()
        # TODO after few tries return error
        timeout = 0
        while already_connected == True:
            vpn.disconnect()
            already_connected = vpn.check_connection()
            timeout += 10
            if timeout == 10:
                while already_connected == True:
                    msg = 'Script can not disconnect from vpn automatically, please do it manually'
                    print(msg)
                    input('Type y if you disconnected manually: ')
                    already_connected = vpn.check_connection()
        vpn.connect()
        already_connected = vpn.check_connection()

        while already_connected == False:
            msg = 'Script can not connect to vpn automatically, please do it manually'
            print(msg)
            input('Type y if you disconnected manually: ')
            already_connected = vpn.check_connection()

    # changes ip in order to make request with different ip than the one buying from

    def extract_date(self, date):
        date_index = re.search(r'\d+', date).start()
        return date[date_index:]

    def translate_month_name(self, date):
        month_translation = {
            'STYCZNIA': 'January',
            'LUTEGO': 'February',
            'MARCA': 'March',
            'KWIETNIA': 'April',
            'MAJA': 'May',
            'CZERWCA': 'June',
            'LIPCA': 'July',
            'SIERPNIA': 'August',
            'WRZEŚNIA': 'September',
            'PAŹDZIERNIKA': 'October',
            'LISTOPADA': 'November',
            'GRUDNIA': 'December',
        }

        date_list = date.split(' ')
        month_pl = date_list[1]
        month_en = month_translation[month_pl]
        date_list[1] = month_en
        final_date = " ".join(date_list)
        return final_date

    def time_difference(self, allegro_date_string):
        today = date.today()
        allegro_date_string = self.translate_month_name(allegro_date_string)
        allegro_date_object = datetime.strptime(allegro_date_string, "%d %B %Y")
        allegro_date_object = allegro_date_object.date()
        allegro_date_difference = today - allegro_date_object
        return allegro_date_difference.days

    def allegro_log_in(self):
        self.browser.get(
            "https://allegro.pl/login/form?authorization_uri=https:%2F%2Fallegro.pl%2Fauth%2Foauth%2Fauthorize%3Fclient_id%3Dtb5SFf3cRxEyspDN%26redirect_uri%3Dhttps:%2F%2Fallegro.pl%2Flogin%2Fauth%3Forigin_url%253D%25252F%26response_type%3Dcode%26state%3DpvLd4b&oauth=true")

        self.browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[2]/button[2]').click()

        self.browser.find_element_by_id("username").clear()
        self.browser.find_element_by_id("username").send_keys(self.login)
        sleep(3)
        self.browser.find_element_by_id("password").clear()
        self.browser.find_element_by_id("password").send_keys(self.password)
        sleep(3)
        self.browser.find_element_by_id("login-button").click()
        sleep(3)

    def get_list_of_accounts(self):
        with open('accounts.json', 'r') as json_file:
            json_data = json.load(json_file)
            return json_data

    def get_account_password(self, login):
        password = keyring.get_password('allegro', login)
        return password

    #return dict of login and date of last submitted feedback,
    #for every login feedback can be submitted only once in 7days
    def get_feedback_dict(self):
        with open('feedback_log', 'rb') as file:
            feedback_dict = pickle.load(file)
            return feedback_dict

    def save_feedback(self, feedback_dict):
        with open('feedback_log', 'wb') as file:
            pickle.dump(feedback_dict, file)

    def perform(self):
        today = date.today()
        accounts_list = self.get_list_of_accounts()
        try:
            feedback_dict = self.get_feedback_dict()
        except FileNotFoundError:
            accounts = list(accounts_list.keys())
            login = accounts[0]
            config_name = self.get_config_name(login, accounts_list)
            self.change_ip(config_name)
            password = self.get_account_password(login)
            allegro = AllegroAutoBuyer(login, password)
            allegro.submit_feedback()
            feedback_dict = {}
            feedback_dict[login] = today

        for login in accounts_list.keys():
            if login not in feedback_dict.keys():
                config_name = self.get_config_name(login, accounts_list)
                self.change_ip(config_name)
                password = self.get_account_password(login)
                allegro = AllegroAutoBuyer(login, password)
                #submit_feedback returns True if was able to submit feedback, if no feedback was available to submit return False
                flag = allegro.submit_feedback()
                if flag:
                    feedback_dict[login] = today
            else:
                config_name = self.get_config_name(login, accounts_list)
                self.change_ip(config_name)
                last_submission = feedback_dict[login]
                elapsed = today - last_submission
                if elapsed >= datetime.timedelta(days=7):
                    password = self.get_account_password(login)
                    allegro = AllegroAutoBuyer(login, password)
                    allegro.submit_feedback()
                    feedback_dict[login] = today
            self.save_feedback(feedback_dict)

if __name__ == "__main__":
    feedback = Submit_Feedback()