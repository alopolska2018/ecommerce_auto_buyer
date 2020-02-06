from AllegroAutoBuyer import AllegroAutoBuyer
# from allegro_auto_buyer.AllegroAutoBuyer import AllegroAutoBuyer
from openvpn.OpenVpn import OpenVpn
import keyring
from datetime import datetime, date
import datetime
import re, json
import pickle
import logging, pathlib

MAIN_DIR = pathlib.Path().absolute()

class Submit_Feedback():
    
    def __init__(self):
        self.logger = logging.Logger('feedback_log')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        main_dir = pathlib.Path().absolute()
        fh = logging.FileHandler('{}/log_files/feedback.log'.format(main_dir))
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.perform()

    def print_and_log(self, msg, log_type='info'):
        print(msg)
        if log_type == 'info':
            self.logger.info(msg)
        else:
            self.logger.error(msg)
        
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
        with open('{}/log/feedback_dict'.format(MAIN_DIR), 'rb') as file:
            feedback_dict = pickle.load(file)
            return feedback_dict

    def save_feedback(self, feedback_dict):
        with open('{}/log/feedback_dict'.format(MAIN_DIR), 'wb') as file:
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
            config_name = self.get_config_name(login, accounts_list)
            msg = 'Using config: {}'.format(config_name)
            self.print_and_log(msg)
            password = self.get_account_password(login)
            
            if login not in feedback_dict.keys():
                self.change_ip(config_name)
                allegro = AllegroAutoBuyer(login, password)
                #submit_feedback returns True if was able to submit feedback, if no feedback was available to submit return False
                flag = allegro.submit_feedback()
                if flag:
                    feedback_dict[login] = today
                    msg = 'Feedback submitted login: {}'.format(login)
                    self.print_and_log(msg)
                else:
                    msg = 'Feedback not submitted login: {}'.format(login)
                    self.print_and_log(msg)
            else:
                last_submission = feedback_dict[login]
                elapsed = today - last_submission
                if elapsed >= datetime.timedelta(days=8):
                    self.change_ip(config_name)
                    allegro = AllegroAutoBuyer(login, password)
                    flag = allegro.submit_feedback()
                    if flag:
                        feedback_dict[login] = today
                        msg = 'Feedback submitted login: {}'.format(login)
                        self.print_and_log(msg)
                    else:
                        msg = 'Feedback not submitted login: {}'.format(login)
                        self.print_and_log(msg)
            self.save_feedback(feedback_dict)

if __name__ == "__main__":
    feedback = Submit_Feedback()