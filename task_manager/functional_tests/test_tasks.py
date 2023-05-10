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
    button_class = 'btn.btn-primary'

    alter_success_after_registration_class = 'alert.alert-success.alert-dismissible.fade.show'
    navigation_statuses_xpath = "//div[@id='navbarToggleExternalContent']//ul[1]//li[2]//a"
    navigation_statuses_link_to_form_css = ".container.wrapper.flex-grow-1 a.nav-link"

    navigation_labels_xpath = "//div[@id='navbarToggleExternalContent']//ul[1]//li[3]//a"

    navigation_tasks_xpath = "//div[@id='navbarToggleExternalContent']//ul[1]//li[4]//a"

    create_task_link_css_selector = ".container.wrapper.flex-grow-1 a"

    name_id = "id_name"
    id_description = "id_description"
    id_status = "id_status"
    status_css = '#id_status option[value="1"]'
    id_executor = "id_executor"
    executor_css = '#id_executor option[value="1"]'
    id_labels = "id_labels"
    labelscss = '#id_labels option[value="1"]'

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
        # registration user1
        self.browser.find_element(By.ID, self.registration_form_field_name_id).send_keys("Tester")
        self.browser.find_element(By.ID, self.registration_form_field_last_name_id).send_keys("Testovich")
        self.browser.find_element(By.ID, self.registration_form_field_username_id).send_keys("testov")
        self.browser.find_element(By.ID, self.registration_form_field_password1_id).send_keys("secretPassword")
        self.browser.find_element(By.ID, self.registration_form_field_password2_id).send_keys("secretPassword")
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()

        # registration user2
        link = self.browser.find_element(By.XPATH, self.registration_link_xpath)
        link.click()
        self.browser.find_element(By.ID, self.registration_form_field_name_id).send_keys("Elon")
        self.browser.find_element(By.ID, self.registration_form_field_last_name_id).send_keys("Mask")
        self.browser.find_element(By.ID, self.registration_form_field_username_id).send_keys("elon")
        self.browser.find_element(By.ID, self.registration_form_field_password1_id).send_keys("secretPassword")
        self.browser.find_element(By.ID, self.registration_form_field_password2_id).send_keys("secretPassword")
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()

        # login
        self.browser.find_element(By.ID, 'id_for_username').send_keys('testov')
        self.browser.find_element(By.ID, 'id_for_password').send_keys('secretPassword')
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()
        print('/login')
        # sleep(5)
        # create status
        self.browser.find_element(By.XPATH, self.navigation_labels_xpath).click()
        self.browser.find_element(By.CSS_SELECTOR, self.navigation_statuses_link_to_form_css).click()
        self.browser.find_element(By.ID, self.name_id).send_keys("label 1")
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()
        self.browser.find_element(By.CSS_SELECTOR, self.navigation_statuses_link_to_form_css).click()
        self.browser.find_element(By.ID, self.name_id).send_keys("label 2")
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()

        # create_label
        self.browser.find_element(By.XPATH, self.navigation_statuses_xpath).click()
        self.browser.find_element(By.CSS_SELECTOR, self.navigation_statuses_link_to_form_css).click()
        self.browser.find_element(By.ID, self.name_id).send_keys("status 1")
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()
        self.browser.find_element(By.CSS_SELECTOR, self.navigation_statuses_link_to_form_css).click()
        self.browser.find_element(By.ID, self.name_id).send_keys("status 2")
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()

        # self.browser.find_element(By.ID, 'id_name')
        self.browser.find_element(By.XPATH, self.navigation_tasks_xpath).click()
        self.browser.find_element(By.CSS_SELECTOR, self.create_task_link_css_selector).click()
        self.browser.find_element(By.ID, self.name_id).send_keys('New task')
        self.browser.find_element(By.ID, self.id_description).send_keys('New task description')
        self.browser.find_element(By.ID, self.id_status).click()
        self.browser.find_element(By.CSS_SELECTOR, self.status_css).click()
        self.browser.find_element(By.CSS_SELECTOR, self.labelscss).click()
        self.browser.find_element(By.CSS_SELECTOR, self.executor_css).click()
        self.browser.find_element(By.CLASS_NAME, self.button_class).click()

        self.browser.find_element(By.ID, self.id_executor).click()
        sleep(5)
        # self.browser.find_element(By.XPATH, self.navigation_tasks_xpath).click()
