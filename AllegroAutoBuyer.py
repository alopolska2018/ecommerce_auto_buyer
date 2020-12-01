from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

class AllegroAutoBuyer:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.browser.set_window_size(1800, 600)
        self.browser.set_window_position(0, 0)
        self.browser.delete_all_cookies()

    def buy_with_login(self, auction_number):
        self.get_product_page(auction_number)
        sleep(3)
        self.accept_cookies_prompt()
        sleep(4)
        self.accept_age_warning()
        sleep(2)
        self.click_buy_it_now()
        sleep(2)
        self.allegro_log_in()
        sleep(2)
        self.fill_buying_form()

    def accept_age_warning(self):
        try:
            elem = self.browser.find_element_by_xpath('//*[text()=\"tak mam 18 lat, idę dalej\"]')
            elem.click()
        except NoSuchElementException:
            pass

    def buy_without_login(self, auction_number):
        self.get_product_page(auction_number)
        sleep(1)
        self.click_buy_it_now()
        sleep(1)
        self.fill_buying_form()

    def click_buy_it_now(self):
        self.browser.find_element_by_xpath('//*[text()="kup teraz"]').click()
        # self.browser.find_element_by_xpath('//button[@id="buy-now-button"]').click()
        # js = 'document.getElementById(\'{}\').click();'.format('buy-now-button')
        # self.browser.execute_script(js)

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
                self.browser.find_element_by_xpath('//span[text()=\'List polecony ekonomiczny\']').click()

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
        sleep(3)

    def prepare_feedback(self):
        self.get_feedback_page()
        sleep(4)
        self.accept_cookies_prompt()
        sleep(2)
        self.allegro_log_in()
        sleep(3)
        self.close_feedback_prompt()

    def check_feedback_availability(self):
        try:
            self.browser.find_element_by_xpath('//p[@class="m-heading m-heading--sm"]')
            return True
        except NoSuchElementException:
            return False

    def close_feedback_prompt(self):
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div[5]/a[1]").click()

    def submit_product_review(self):
        self.browser.find_element_by_xpath("//span[6]").click()
        self.browser.find_element_by_xpath("//button[@type='button'])[13]").click()

    def submit_feedback(self, allegro_login):
        self.prepare_feedback()
        sleep(3)
        try:
            self.submit_product_review()
        except:
            pass
        self.get_feedback_page()
        feedback_available = self.check_feedback_availability()
        if feedback_available:
            try:
                current_feedback = self.browser.find_element_by_xpath('//p[@class="m-heading m-heading--sm"]').text
                current_feedback = current_feedback.lower()
            except:
                pass

            while current_feedback != allegro_login:
                try:
                    self.browser.find_element_by_xpath('//a[@class="m-link m-link--non-visited m-color-teal"]').click()
                except NoSuchElementException:
                    print('No feedback entry for account {}'.format(allegro_login))
                    self.browser.close()
                    return False
                sleep(2)
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
                sleep(2)
                self.browser.close()
                return True
            except NoSuchElementException:
                self.browser.close()
                return False
                pass
        self.browser.close()
        return False