from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class TestTaskManagerRegistration(StaticLiveServerTestCase):
    registration_link_xpath = "//div[@id='navbarToggleExternalContent']//ul[2]//li[2]//a"
    registration_form_css_path = 'form[action="/users/create/"]'
    registration_form_field_name_id = 'id_first_name'
    registration_form_field_last_name_id = 'id_last_name'
    registration_form_field_username_id = 'id_username'
    registration_form_field_password1_id = 'id_password1'
    registration_form_field_password2_id = 'id_password2'
    registration_form_field_button_class = 'btn.btn-primary'
    alter_success_after_registration_class = 'alert.alert-success.alert-dismissible.fade.show'

    def setUp(self) -> None:
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.set_window_size(1920, 1080)
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.close()

    def test_find_registration_link(self):
        self.browser.get(self.live_server_url)
        reg = WebDriverWait(
            self.browser, 12).until(EC.text_to_be_present_in_element(
             (
              By.XPATH, self.registration_link_xpath), text_='Registration'
            )
        )
        self.assertTrue(reg)

    def test_click_registration_link(self):
        link = self.browser.find_element(By.XPATH, self.registration_link_xpath)
        link.click()
        form = self.browser.find_element(By.CSS_SELECTOR, self.registration_form_css_path)
        self.assertTrue(form)

    def test_click_input_data(self):
        link = self.browser.find_element(By.XPATH, self.registration_link_xpath)
        link.click()
        self.browser.find_element(By.ID, self.registration_form_field_name_id).send_keys("Tester")
        self.browser.find_element(By.ID, self.registration_form_field_last_name_id).send_keys("Testovich")
        self.browser.find_element(By.ID, self.registration_form_field_username_id).send_keys("testov")
        self.browser.find_element(By.ID, self.registration_form_field_password1_id).send_keys("secretPassword")
        self.browser.find_element(By.ID, self.registration_form_field_password2_id).send_keys("secretPassword")

    def test_click_input_data_and_registrate(self):
        link = self.browser.find_element(By.XPATH, self.registration_link_xpath)
        link.click()
        self.browser.find_element(By.ID, self.registration_form_field_name_id).send_keys("Tester")
        self.browser.find_element(By.ID, self.registration_form_field_last_name_id).send_keys("Testovich")
        self.browser.find_element(By.ID, self.registration_form_field_username_id).send_keys("testov")
        self.browser.find_element(By.ID, self.registration_form_field_password1_id).send_keys("secretPassword")
        self.browser.find_element(By.ID, self.registration_form_field_password2_id).send_keys("secretPassword")
        self.browser.find_element(By.CLASS_NAME, self.registration_form_field_button_class).click()
        message = WebDriverWait(
            self.browser, 12).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, self.alter_success_after_registration_class),
                                             'User has been registered successfully')
        )
        self.assertTrue(message)

    def test_login(self):
        self.test_click_input_data_and_registrate()
        self.browser.find_element(By.ID, 'id_for_username').send_keys('testov')
        self.browser.find_element(By.ID, 'id_for_password').send_keys('secretPassword')
        self.browser.find_element(By.CLASS_NAME, self.registration_form_field_button_class).click()
        message = WebDriverWait(
            self.browser, 12).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, self.alter_success_after_registration_class),
                                             'You are login')
        )
        self.assertTrue(message)
