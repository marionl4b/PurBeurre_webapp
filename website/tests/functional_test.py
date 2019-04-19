from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    """Test new visitor"""
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_register_substitute_for_search_product(self):
        #  Lily goes to the purbeurre platform for the first time
        self.browser.get(self.live_server_url)

        #  It displays the home page and she locates 2 search input
        search_1 = self.browser.find_element_by_id('first-search')
        search_2 = self.browser.find_element_by_id('second-search')
        assert search_1 and search_2

        #  She launches a search for nutella
        search_1.send_keys('nutella')
        search_1.send_keys(Keys.ENTER)

        #  The application returns the results page
        search_title = self.browser.find_element_by_tag_name('h1').text
        assert search_title == "Résultats pour Nutella"

        #  Lily wants to register a product
        #  She must authenticate
        #  The application offers him to create an account via a registration form
        #  Lily fill in the form and create a new account
        #  It is redirected to my products page
        self.fail('Finish the test!')

    # def test_user_can_retrieve_favorites_products(self):
    #     pass
        #  Lily wants to find her favorite products on the purbeurre platteforme
        #  She clicks on the icon my products
        #  She must identify herself
        #  She sees these favorite products and can access the details of these products
