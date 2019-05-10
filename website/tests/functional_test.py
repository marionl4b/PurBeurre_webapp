from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    """Test new visitor scenario"""
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
        time.sleep(5)

        #  The application returns the results page
        search_title = self.browser.find_element_by_tag_name('h1').text
        assert search_title == "RÉSULTATS POUR NUTELLA"

        #  Lily wants to register a product
        fav_btn = self.browser.find_element_by_class_name('favorite')
        assert fav_btn

        add_fav_btn = fav_btn.find_element_by_css_selector(":first-child")
        add_fav_btn.click()
        time.sleep(1)

        #  She must authenticate
        #  The application offers her to create an account via a registration form
        register_link = self.browser.find_element_by_link_text("S'enregistrer")
        assert register_link

        register_link.click()
        time.sleep(1)

        #  Lily fill in the form and create a new account
        page_title = self.browser.find_element_by_tag_name('h1').text
        assert page_title == "S'ENREGISTRER"

        input_name = self.browser.find_element_by_id('id_username')
        input_email = self.browser.find_element_by_id('id_email')
        input_password1 = self.browser.find_element_by_id('id_password1')
        input_password2 = self.browser.find_element_by_id('id_password2')
        submit = self.browser.find_element_by_class_name('btn-primary')
        input_name.send_keys('lily')
        input_email.send_keys('lily@mail.com')
        input_password1.send_keys('lily12345')
        input_password2.send_keys('lily12345')
        submit.click()
        time.sleep(1)

        # She must login
        page_title = self.browser.find_element_by_tag_name('h1').text
        assert page_title == "SE CONNECTER"

        input_name = self.browser.find_element_by_id('id_username')
        input_password = self.browser.find_element_by_id('id_password')
        submit = self.browser.find_element_by_class_name('btn-primary')
        input_name.send_keys('lily')
        input_password.send_keys('lily12345')
        submit.click()
        time.sleep(1)

        #  She re-launches a search for nutella on the homepage
        page_title = self.browser.find_element_by_tag_name('h1').text
        assert page_title == "Du gras, oui, mais de qualité !"
        search_1 = self.browser.find_element_by_id('first-search')
        search_1.send_keys('nutella')
        search_1.send_keys(Keys.ENTER)
        time.sleep(5)

        #  The application returns the results page
        search_title = self.browser.find_element_by_tag_name('h1').text
        assert search_title == "RÉSULTATS POUR NUTELLA"

        #  Lily wants to register a product
        fav_btn = self.browser.find_element_by_class_name('favorite')
        assert fav_btn

        add_fav_btn = fav_btn.find_element_by_css_selector(":first-child")
        add_fav_btn.click()
        time.sleep(1)

        #  It is redirected to my products page
        fav_name = self.browser.find_element_by_tag_name('h6').text
        assert fav_name == "Kiri à la crème de lait (12 Portions)"
        self.fail('Finish the test!')
