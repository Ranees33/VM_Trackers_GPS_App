import time

import pytest
from Tools.scripts.var_access_benchmark import B
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class TestLoginFunctionality:

    @pytest.fixture(scope="class")
    def launch_setup(self):
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(20)
        driver.get("https://tracker.vmmaps.com/login")
        yield driver
        driver.close()

    def test_login_field_elements_displayed(self, launch_setup):
        driver = launch_setup
        driver.refresh()
        email_field = driver.find_element(By.XPATH, "//input[@class='input-field']")
        if email_field.is_displayed():
            print("Email field is displayed")
        else:
            print("Email field is not displayed")

        password_field = driver.find_element(By.ID, "pass")
        if password_field.is_displayed():
            print("Password field is displayed")
        else:
            print("Password field is not displayed")

        forgotpass_field = driver.find_element(By.XPATH, "//div[text()='Forgot Password ?']")
        if forgotpass_field.is_displayed():
            print("Forgot password option field is displayed")
        else:
            print("Forgot password option field is not displayed")

        submit_Btn_field = driver.find_element(By.ID, "loginSubmit")
        if submit_Btn_field.is_displayed():
            print("Submit button field is displayed")
        else:
            print("Password field is not displayed")

    @pytest.mark.parametrize(
        "email, password, expected_result",
        [
            ("tonyboniee@gmail.com", "Ranees@12345", "Succuessfully Registered")
        ]
    )
    def test_login_and_logout(self, launch_setup, email, password, expected_result):
        driver = launch_setup
        driver.refresh()
        # wait = WebDriverWait(driver, 20)
        wait = WebDriverWait(driver, 30, 10, ignored_exceptions=[ElementClickInterceptedException])
        driver.find_element(By.XPATH, "//input[@class='input-field']").clear()
        enter_Email = driver.find_element(By.XPATH, "//input[@class='input-field']")
        enter_Email.send_keys(email)
        driver.find_element(By.ID, "pass").clear()
        enter_Password = driver.find_element(By.ID, "pass")
        enter_Password.send_keys(password)
        driver.find_element(By.ID, "loginSubmit").click()
        try:
            user_profile = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='dropdown']")))
            user_profile.click()
        except Exception as e:
            print(e)
        driver.find_element(By.XPATH, "//p[text()='Log Out']").click()

    @pytest.mark.parametrize(
        "email, password, expected_result",
        [
            ("tonyboniee@gmail.com", "Raneessu@123456", "Cannot login at the moment"),
            # Username already exists
            ("tonybonniee@gmail.in", "Ranees@12345", "Cannot login at the moment"),
            # Email already registered
            ("tonybonniee@gmaill.con", "Raneessn@123456", "Cannot login at the moment"),
            # Invalid email format
            ("tonyboniee@gmail.com", "", "Please Enter Password"),
            # Passwords do not match
            ("", "Ranees@12345", "Please Enter Valid Email"),
            # All fields empty
            ("", "", "Please Enter Valid Email"),
            # Email field empty
            ("TonyBoniee@Gmail.Com", "Ranees@12345", "Cannot login at the moment"),
            # Password field empty
            ("('tonyboniee@gmail.com'):", "Ranees: @'12345'", "Please Enter Valid Email"),
            # Password field empty
            ("<tonyboniee@gmail.com>", "Ranees@12345", "Please Enter Valid Email"),
            # Password field empty
            ("tonyboniee@gmail.com", "Rn@!@#$%", "Cannot login at the moment"),
            # Password field empty
        ]
    )
    def test_login(self, launch_setup, email, password, expected_result):
        driver = launch_setup
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, "//input[@class='input-field']").clear()
        enter_Email = driver.find_element(By.XPATH, "//input[@class='input-field']")
        enter_Email.send_keys(email)
        driver.find_element(By.ID, "pass").clear()
        enter_Password = driver.find_element(By.ID, "pass")
        enter_Password.send_keys(password)
        driver.find_element(By.ID, "loginSubmit").click()

        # Use explicit wait to handle different scenarios
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_result}')]"))
            )
            assert expected_result in driver.page_source
        except:
            assert False, f"Expected result '{expected_result}' not found in page source"

    if __name__ == "__main__":
        pytest.main()
