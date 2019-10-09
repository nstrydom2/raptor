import lxml, requests, csv, os.path
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options


def string_format_urls(a_tags):
    result_str = ''
    for a_tag in a_tags:
        result_str += a_tag.text + '\n'

    return result_str


def gen_element_dict(elements):
    target_dict = []

    for element in elements:
        target_dict.append(element.get_attribute('href'))

    return target_dict


class Bot:
    def __init__(self):
        # Below needs to be changed for production
        geckdriver_path = r'/home/ghost/Drivers/geckodriver'

        options = Options()
        #options.headless = True

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
                a_elements = gen_element_dict(results_element.find_elements_by_tag_name('a'))

                for element in a_elements:
                    self.driver.get(element)
                    self.wait(5)

                    self.scrape_target_page(self.driver.page_source)

                    # Sleep for n seconds and then continue
                    time.sleep(10)

                    self.driver.back()
                    self.wait(5)

                # Sleep for n seconds and then continue
                time.sleep(20)

        except Exception as ex:
            print(str(ex))

        finally:
            self.driver.close()

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
            csv_file.close()

    def scrape_target_page(self, doc):
        try:
            soup = BeautifulSoup(doc, 'lxml')
            title_element = soup.select('.col-lg-8 > div:nth-child(1) > div:nth-child(1)')[0]
            div_element = soup.select('div.col:nth-child(1)')[0]
            li_tags = div_element.find_all('li')[0]
            a_tags = div_element.find_all('a')

            college_name = ''
            booker_phone = ''
            booker_email = ''
            links = []

            try:
                college_name = title_element.contents[0].text.strip()
                booker_phone = li_tags.contents[1].strip()
                booker_email = li_tags.contents[0].text
                links = string_format_urls(a_tags)

            except Exception as parse_ex:
                print(str(parse_ex))

            with open(r'data.csv', 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([college_name, booker_phone, booker_email, links])
            csv_file.close()

        except Exception as ex:
            print(str(ex))

    def wait(self, delay=3):
        try:
            self.driver.implicitly_wait(delay)

        except Exception as ex:
            print(str(ex))


