import lxml, requests, csv, os.path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options

class Bot:
    def __init__(self):
        # Below needs to be changed for production
        geckdriver_path = r'/home/ghost/Drivers/geckodriver'

        options = Options()
        options.headless = True

        browser_profile = webdriver.FirefoxProfile()
        browser_profile.set_preference('dom.webnotifications.enabled', False)
        self.driver = webdriver.Firefox(executable_path=geckdriver_path, firefox_profile=browser_profile,
                                        firefox_options=options)

    def scrape_all(self):
        usr = ''
        pwd = ''

        login_url = 'https://www.indieonthemove.com/login'
        main_page_url = 'https://www.indieonthemove.com/colleges'

        try:
            # Check if csv is present
            self.check_csv()

            # Login to the web site to get the cookie properly
            self.init_login(login_url, usr, pwd)

            for index in range(1, 70):
                self.driver.get(main_page_url + '?page={0}'.format(index))
                self.wait()

                results_element = self.driver.find_element_by_css_selector('.mt-1')

                for element in results_element.find_elements_by_tag_name('a'):
                    self.driver.get(element.get_attribute('href'))
                    self.wait()

                    self.scrape_target_page(self.driver.page_source)

        except Exception as ex:
            print(str(ex))

    def init_login(self, login_url, usr, pwd):
        self.driver.get(login_url)
        self.wait()

        login = self.driver.find_element_by_id('email')
        pword = self.driver.find_element_by_id('password')
        submit_button = \
            self.driver.find_element_by_xpath('/html/body/div/div[1]/div/div/div/div/div/div[2]/form/div[4]/button')

        login.send_keys(usr)
        pword.send_keys(pwd)
        submit_button.click()
        self.wait()

    def check_csv(self):
        if not os.path.exists('data.csv'):
            with open(r'data.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Name', 'Phone', 'Email', 'Links'])

    def scrape_target_page(self, doc):
        try:
            soup = BeautifulSoup(doc, 'lxml')
            title_element = soup.select('.col-lg-8 > div:nth-child(1) > div:nth-child(1)')
            div_element = soup.select('div.col:nth-child(1)')
            a_tags = div_element.find_all('a')

            with open(r'data.csv', 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([title_element.find('h4').text,
                                     self.string_formatre, '', ''])

        except Exception as ex:
            print(str(ex))

    def wait(self, delay=3):
        try:
            self.driver.implicitly_wait(delay)

        except Exception as ex:
            print(str(ex))


