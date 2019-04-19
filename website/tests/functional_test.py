from django.test import LiveServerTestCase
from selenium import webdriver
import pytest


class NewVisitorTest(LiveServerTestCase):
    """Test new visitor"""
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_homepage(self):
        #  Lily goes to the purbeurre platform for the first time
        self.browser.get(self.live_server_url)

        #  It displays the home page and she locates the search
        #  She launches a search
        #  The application returns the results page
        #  Lily wants to register a product
        #  She must authenticate
        #  The application offers him to create an account via a registration form
        #  Lily fill in the form and create a new account
        #  It is redirected to my products page
        self.fail('Finish the test!')


class UserProductsTest(LiveServerTestCase):
    """Test retrieve user favorites products"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # Lily wants to find her favorite products on the purbeurre platteforme
    # She clicks on the icon my products
    # She must identify herself
    # She sees these favorite products and can access the details of these products
