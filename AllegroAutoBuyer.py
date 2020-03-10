from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException

class AllegroAutoBuyer:

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

    def buy_with_login(self, auction_number):
        self.get_product_page(auction_number)
        sleep(1)
        self.accept_cookies_prompt()
        sleep(1)
        self.click_buy_it_now()
        sleep(1)
        self.allegro_log_in()
        sleep(2)
        self.fill_buying_form()

    def buy_without_login(self, auction_number):
        self.get_product_page(auction_number)
        sleep(1)
        self.click_buy_it_now()
        sleep(1)
        self.fill_buying_form()

    def click_buy_it_now(self):
        self.browser.find_element_by_xpath('//button[@data-analytics-interaction-label="PreBuyNow"]').click()

    def allegro_log_in(self):
        self.browser.find_element_by_id("username").clear()
        self.browser.find_element_by_id("username").send_keys(self.login)
        sleep(3)
        self.browser.find_element_by_id("password").clear()
        self.browser.find_element_by_id("password").send_keys(self.password)
        sleep(3)
        self.browser.find_element_by_id("login-button").click()
        sleep(3)

    def search_product_allegro(self, auction_number):
        sleep(5)
        self.browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_14uqc", " " ))]').send_keys(auction_number)
        sleep(3)
        self.browser.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Wszystkie kategorie'])[1]/following::button[1]").click()
        sleep(3)

    def get_product_page(self, auction_number):
        self.browser.get('https://allegro.pl/oferta/{}'.format(auction_number))

    def accept_cookies_prompt(self):
        self.browser.find_element_by_xpath('//button[@type=\'button\'][@data-role=\'accept-consent\']').click()

    def fill_buying_form(self):
        try:
            self.browser.find_element_by_xpath('//span[text()=\'List ekonomiczny\']').click()
        except Exception:
            try:
                self.browser.find_element_by_xpath('//span[text()=\'List polecony priorytetowy\']').click()
            except Exception:
                self.browser.find_element_by_xpath('//span[text()=\'List polecony ekonomiczny\']')

        sleep(3)
        self.browser.find_element_by_xpath('//div[contains(@class, \'cash-transfer\')]').click()
        sleep(3)
        self.browser.find_element_by_xpath('//div[contains(text(),\'Płacę przelewem tradycyjnym\')]').click()
        sleep(3)
        self.browser.find_element_by_xpath('//span[contains(text(),\'kupuję i płacę\')]').click()
        sleep(5)

    def home_page(self):
        self.browser.get('https://allegro.pl/')

    def close_browser(self):
        self.browser.close()

    def get_feedback_page(self):
        self.browser.get('https://allegro.pl/user-rating-landing-page/index')


    def submit_feedback(self, allegro_login):
        self.get_feedback_page()
        sleep(4)
        self.accept_cookies_prompt()
        sleep(2)
        self.allegro_log_in()
        sleep(3)
        current_feedback = self.browser.find_element_by_xpath('//p[@class="m-heading m-heading--sm"]').text
        current_feedback = current_feedback.lower()

        while current_feedback != allegro_login:
            try:
                self.browser.find_element_by_xpath('//a[@class="m-link m-link--non-visited m-color-teal"]').click()
            except NoSuchElementException:
                print('No feedback entry for account {}'.format(allegro_login))
                return False
            current_feedback = self.browser.find_element_by_xpath('//p[@class="m-heading m-heading--sm"]').text
            current_feedback = current_feedback.lower()

        try:
            self.browser.find_element_by_xpath('//*[text()=\' Polecam \']').click()
        except NoSuchElementException:
            pass

        sleep(2)
        #clicking stars
        try:
            self.browser.find_element_by_xpath(
                "//div[@id='rating-module']/app-rate-order/div/section/div[2]/app-rating-seller-form/section/section/div/div/div[2]/app-description-star-rating/div/div/span[5]/i").click()
        except NoSuchElementException:
            pass

        sleep(2)
        try:
            self.browser.find_element_by_xpath(
                "//div[@id='rating-module']/app-rate-order/div/section/div[2]/app-rating-seller-form/section/section/div[2]/div/div[2]/app-delivery-cost-star-rating/div/div/span[5]/i").click()
        except NoSuchElementException:
            pass
        sleep(3)
        try:
            self.browser.find_element_by_xpath(
                "//div[@id='rating-module']/app-rate-order/div/section/div[2]/app-rating-seller-form/section/section/div[3]/div/div[2]/app-service-star-rating/div/div/span[5]/i").click()
        except NoSuchElementException:
            pass
        sleep(5)
        #clicking submit
        try:
            self.browser.find_element_by_xpath('//button[text()=\' wystaw ocenę \']').click()
            self.browser.close()
            return True
        except NoSuchElementException:
            self.browser.close()
            return False
            pass