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

    def perform(self, auction_number):
        self.get_product_page(auction_number)
        sleep(2)
        self.click_buy_it_now()
        sleep(2)
        self.allegro_log_in()
        sleep(2)
        self.fill_buying_form()
        self.close_browser()
    
    def click_buy_it_now(self):
        self.browser.find_element_by_xpath('//button[@data-analytics-interaction-label="PreBuyNow"]').click()

    def allegro_log_in(self):
        # self.browser.get(
        #     "https://allegro.pl/login/form?authorization_uri=https:%2F%2Fallegro.pl%2Fauth%2Foauth%2Fauthorize%3Fclient_id%3Dtb5SFf3cRxEyspDN%26redirect_uri%3Dhttps:%2F%2Fallegro.pl%2Flogin%2Fauth%3Forigin_url%253D%25252F%26response_type%3Dcode%26state%3DpvLd4b&oauth=true")
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
        sleep(2)
        #accept prompt about cookies
        self.browser.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='nie zgadzam się'])[1]/following::button[1]").click()

    def fill_buying_form(self):
        try:
            self.browser.find_element_by_xpath(
                "#m-soap-103-label").click()
        except NoSuchElementException:
            pass
        # self.browser.find_element_by_xpath('/html/body/div/div[2]/section/div/section/ui-view/section/section/section/form/section[2]/payments-methods/ng-form/div/m-soap-group/div/m-payment-soap[1]/m-soap/div[2]/label/div[2]/div/div').click()
        self.browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Listy i paczki pocztowe'])[1]/following::label[1]").click()
        sleep(3)
        try:
            self.browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Finanse'])[1]/following::div[7]").click()
        except NoSuchElementException:
            self.browser.find_element_by_xpath("//label[contains(@id,'m-soap-')]/div[2]/div/div").click()
        sleep(3)
        self.browser.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='Płacę z iPKO'])[1]/following::label[1]").click()
        # sleep(5)
        # self.browser.find_element_by_xpath("/html/body/div/div[2]/section/div/section/ui-view/section/section/aside/div/div/summary-panel/section/section[3]/div/div/buy-button/button/span[2]/span").click()
    def home_page(self):
        self.browser.get('https://allegro.pl/')

    def close_browser(self):
        self.browser.close()

    def submit_feedback(self):
        self.browser.get('https://allegro.pl/user-rating-landing-page/index')
        sleep(5)
        # allegro_date_string = self.browser.find_element_by_xpath('//p[@class=\'m-type m-type--caption\']').text
        # allegro_date_string = self.extract_date(allegro_date_string)
        # allegro_date_difference = self.time_difference(allegro_date_string)
        # self.browser.find_element_by_css_selector('div.landing-page-flex-wrapper:nth-child(2) div.landing-page-content-wrapper:nth-child(2) div.main-wrapper:nth-child(2) div.m-desk:nth-child(2) div.m-desk__content div.user-rating-wrapper div.user-rating-wrapper div.m-card section.m-grid.m-grid--v-align.m-grid__col--spacer-bottom div.m-grid__col.m-grid__col--12:nth-child(2) div.m-grid div.m-grid__col.m-grid__col--12.thumbs-wrapper div.m-margin-top-16 > span.m-type.m-type--tiny.m-color-gray.thumbContainer:nth-child(1)').click()
        # self.browser.find_element_by_xpath('/html/body/div/div[2]/app-root/app-dashboard/div[2]/app-order-to-rate/div/div/div/div/app-rate-order/div/section/div[2]/app-rating-seller-form/section/app-rating-seller-form-header/section/div[2]/div/div/div[1]/span[1]/i').click()
        # self.browser.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='Czy polecasz tego sprzedawcę?'])[1]/following::span[1]").click()

        try:
            self.browser.find_element_by_xpath(
                u"(.//*[normalize-space(text()) and normalize-space(.)='Czy polecasz tego sprzedawcę?'])[1]/following::span[1]").click()
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
            self.browser.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='pomiń ten zakup'])[1]/following::button[1]").click()
            return True
        except NoSuchElementException:
            pass

        self.browser.close()