from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date
import re

class Submit_Feedback():
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.options = Options()
        self.options.headless = False
        self.browser_locale = 'pl'
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference('intl.accept_languages', self.browser_locale)

        self.browser = webdriver.Firefox(options=self.options, firefox_profile=self.profile)
        self.browser.delete_all_cookies()
        self.browser.set_window_size(1800, 600)
        self.browser.set_window_position(0, 0)
        self.accept_next_alert = True
        self.allegro_log_in()
        self.perform()

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

    def submit_feedback(self):
        self.browser.get('https://allegro.pl/user-rating-landing-page/index')
        allegro_date_string = self.browser.find_element_by_xpath('//p[@class=\'m-type m-type--caption\']').text
        allegro_date_string = self.extract_date(allegro_date_string)
        allegro_date_difference = self.time_difference(allegro_date_string)
        if allegro_date_difference >= 30:
            self.browser.find_element_by_xpath('//span[@class=\'m-type m-type--tiny m-color-gray thumbContainer\']').click()
            #clicking stars
            self.browser.find_element_by_xpath(
                "//div[@id='rating-module']/app-rate-order/div/section/div[2]/app-rating-seller-form/section/section/div/div/div[2]/app-description-star-rating/div/div/span[5]/i").click()
            self.browser.find_element_by_xpath(
                "//div[@id='rating-module']/app-rate-order/div/section/div[2]/app-rating-seller-form/section/section/div[2]/div/div[2]/app-delivery-cost-star-rating/div/div/span[5]/i").click()
            self.browser.find_element_by_xpath(
                "//div[@id='rating-module']/app-rate-order/div/section/div[2]/app-rating-seller-form/section/section/div[3]/div/div[2]/app-service-star-rating/div/div/span[5]/i").click()

        else:
            self.browser.find_element_by_xpath('//a[@class=\'m-link m-link--non-visited m-color-teal\']').click()
            
    def perform(self):
        self.submit_feedback()

feed = Submit_Feedback('lisi3ck4@gmail.com', 'StarWarsVader2020!')
