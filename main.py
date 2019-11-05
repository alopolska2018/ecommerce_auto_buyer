from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException



class AllegroAutoBuyer:

    def __init__(self):
        self.login = 'lisi3ck4@gmail.com'
        self.password = 'StarWarsVader2020!'
        # self.website = input('Enter auction number: ')
        # self.user = input('choose account to use [Type 1 for : ugreen]')
        self.options = Options()
        self.options.headless = False
        self.browser = webdriver.Firefox(options=self.options)
        self.browser.set_window_size(1800, 600)
        self.browser.set_window_position(0, 0)
        self.accept_next_alert = True
        self.allegro_log_in()

    def perform(self, auction_number):
        self.search_product_allegro(auction_number)
        self.buy_allegro()
        self.home_page()
        # self.login()
        # sleep(10)
        # self.search()

    def read_file(self, filename):

        file = open(filename, 'r')

        auction_numbers = []

        for line in file:
            line = line.strip()
            auction_numbers.append(line)

        return auction_numbers

    def allegro_log_in(self):
        self.browser.get(
            "https://allegro.pl/login/form?authorization_uri=https:%2F%2Fallegro.pl%2Fauth%2Foauth%2Fauthorize%3Fclient_id%3Dtb5SFf3cRxEyspDN%26redirect_uri%3Dhttps:%2F%2Fallegro.pl%2Flogin%2Fauth%3Forigin_url%253D%25252F%26response_type%3Dcode%26state%3DpvLd4b&oauth=true")

        self.browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[2]/div/div[2]/button').click()

        self.browser.find_element_by_id("username").clear()
        self.browser.find_element_by_id("username").send_keys(self.login)
        sleep(3)
        self.browser.find_element_by_id("password").clear()
        self.browser.find_element_by_id("password").send_keys(self.password)
        sleep(3)
        self.browser.find_element_by_id("login-button").click()
        sleep(3)

    def search_product_allegro(self, auction_number):


        # self.browser.find_element_by_css_selector("._d25db_31-XG").send_keys(auction_number)
        self.browser.find_element_by_xpath("/html/body/div[2]/div[3]/nav/div/div[1]/div/div/form/input").send_keys(auction_number)
        sleep(3)
        self.browser.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Wszystkie kategorie'])[1]/following::button[1]").click()
        sleep(3)

    def buy_allegro(self):
        # self.browser.find_element_by_name("quantity").click()
        # self.browser.find_element_by_name("quantity").clear()
        # sleep(3)
        # self.browser.find_element_by_name("quantity").send_keys("1")
        self.browser.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Dodaj do koszyka'])[1]/following::button[1]").click()
        sleep(3)
        try:
            self.browser.find_element_by_xpath(
                "/html/body/div/div[2]/section/div/section/ui-view/section/section/section/form/delivery-section/section/section/ng-form/delivery-bundle/section[1]/div[2]/delivery-options/delivery-methods-groups/section/ng-form/div[1]/div/div/div[1]/div/div/label").click()
        except NoSuchElementException:
            pass
        sleep(5)
        try:
            self.browser.find_element_by_xpath("/html/body/div/div[2]/section/div/section/ui-view/section/section/section/form/section[2]/payments-methods/ng-form/div[1]/m-soap-group/div/m-payment-soap[2]/m-soap/div[2]/label/div[2]/div/div").click()
        except NoSuchElementException:
            pass
        sleep(5)
        self.browser.find_element_by_xpath("/html/body/div/div[2]/section/div/section/ui-view/section/section/aside/div/div/summary-panel/section/section[3]/div/div/buy-button/button/span[2]/span").click()
    def home_page(self):
        self.browser.get('https://allegro.pl/')



auto_buyer = AllegroAutoBuyer()

# auto_buyer.perform('6570839702')

# site = input('Which site you want to buy from [Type: 1 for Allegro]: ')
#
choice = input('Read auctions numbers from file? [y/n]: ')

if choice == 'y':

    filename = input('Enter filename [{file must be inside script dir} ex. auctions.txt]: ')
    auction_numbers = auto_buyer.read_file(filename)

    for auction in auction_numbers:
        auto_buyer.perform(auction)

elif choice == 'n':

    auction = input('Enter auction number: ')
    auto_buyer.perform(auction)

else:
    print('Wrong choice')