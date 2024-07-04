import time

import pytest
from Tools.scripts.var_access_benchmark import B
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestForgotPassword:

    @pytest.fixture(scope="class")
    def setup(self):
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(10)
        driver.get("https://tracker.vmmaps.com/login")
        yield driver
        driver.quit()

    @pytest.mark.parametrize(
        "email, expected_result",
        [
            ("tonyboni@gmail.com", "Cannot reset password"),
            ("tonyboniee@gmail", "Invalid email"),
            ("", "Email cannot be empty"),  # Invalid email format
            ("('tonyboniee@gmail.com'):", "Invalid email"),
            ("TonyBoniee@Gmail.Com", "Cannot reset password"),
            (" tonyboniee@gmail.com ", "Cannot reset password"),
            ("tonyboniee@gmail.con", "Cannot reset password"),  # Email field empty
        ]
    )
    def test_forgot_password(self, setup, email, expected_result):
        driver = setup
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, "//div[text()='Forgot Password ?']").click()
        driver.find_element(By.XPATH, "//input[@class='input-field']").clear()
        enter_Email = driver.find_element(By.XPATH, "//input[@class='input-field']")
        enter_Email.send_keys(email)
        driver.find_element(By.XPATH, "//button[@class='sc-gLLuof kuxdqO']").click()

        # Use explicit wait to handle different scenarios
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_result}')]"))
            )
            assert expected_result in driver.page_source
        except:
            assert False, f"Expected result '{expected_result}' not found in page source"

    @pytest.mark.parametrize(
        "email, expected_result",
        [
            ("tonyboniee@gmail.com", "Check your email account for reset link!"),
        ]
    )
    def test_forgot_password_and_sent_okay(self, setup, email, expected_result):
        driver = setup
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, "//div[text()='Forgot Password ?']").click()
        driver.find_element(By.XPATH, "//input[@class='input-field']").clear()
        enter_Email = driver.find_element(By.XPATH, "//input[@class='input-field']")
        enter_Email.send_keys(email)
        driver.find_element(By.XPATH, "//button[@class='sc-gLLuof kuxdqO']").click()
        driver.find_element(By.XPATH, "//button[@class='sc-gLLuof eAgKZT']").click()

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
