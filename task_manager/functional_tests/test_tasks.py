from time import sleep

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


ru_headers = {"intl.accept_languages": "ru"}


class TestTask(StaticLiveServerTestCase):
    registration_link_xpath = "//div[@id='navbarToggleExternalContent']//ul[2]//li[2]//a"
    registration_form_css_path = 'form[action="/users/create/"]'
    registration_form_field_name_id = 'id_first_name'
    registration_form_field_last_name_id = 'id_last_name'
    registration_form_field_username_id = 'id_username'
    registration_form_field_password1_id = 'id_password1'
    registration_form_field_password2_id = 'id_password2'
    registration_form_field_button_class = 'btn.btn-primary'
    alter_success_after_registration_class = 'alert.alert-success.alert-dismissible.fade.show'
    navigation_tasks_xpath = "//div[@id='navbarToggleExternalContent']//ul[1]//li[4]//a"
    create_task_link_css_selector = ".container.wrapper.flex-grow-1 a"

    def setUp(self) -> None:
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option('prefs', ru_headers)

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.close()

    def test_login(self):
        link = self.browser.find_element(By.XPATH, self.registration_link_xpath)
        link.click()
        self.browser.find_element(By.ID, self.registration_form_field_name_id).send_keys("Tester")
        self.browser.find_element(By.ID, self.registration_form_field_last_name_id).send_keys("Testovich")
        self.browser.find_element(By.ID, self.registration_form_field_username_id).send_keys("testov")
        self.browser.find_element(By.ID, self.registration_form_field_password1_id).send_keys("secretPassword")
        self.browser.find_element(By.ID, self.registration_form_field_password2_id).send_keys("secretPassword")
        self.browser.find_element(By.CLASS_NAME, self.registration_form_field_button_class).click()
        self.browser.find_element(By.ID, 'id_for_username').send_keys('testov')
        self.browser.find_element(By.ID, 'id_for_password').send_keys('secretPassword')
        self.browser.find_element(By.CLASS_NAME, self.registration_form_field_button_class).click()
        self.browser.find_element(By.XPATH, self.navigation_tasks_xpath).click()
        self.browser.find_element(By.CSS_SELECTOR, self.create_task_link_css_selector).click()
        sleep(50)
        # self.browser.find_element(By.XPATH, self.navigation_tasks_xpath).click()
