import unittest

from web_scraper import Bot


class WebScraperTest(unittest.TestCase):
    def test_scraping_end_page(self):
        bot = Bot()

        try:
            bot.scrape_all()

        except Exception as ex:
            print(str(ex))

