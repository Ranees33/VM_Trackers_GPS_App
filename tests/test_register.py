import time

import pytest
from Tools.scripts.var_access_benchmark import B
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestRegisterFunctionality:

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
        "username, email, phone_number, password, expected_result",
        [
            ("arkranees", "tonyboniee@gmail.com", "9047864060", "Ranees@12345", "Successfully Registered"),
            # Valid registration
            ("arkranees", "tonyboniee@gmail.com", "9047864060", "Ranees@12345", "User mobile or email already exists"),
            # Username already exists
            ("arkranees", "tonyboniee@gmail.com", "9047864060", "Ranees@12345", "User mobile or email already exists"),
            # Email already registered
            ("arkranees", "tonyboniee@gmail.", "9047864060", "Ranees@12345", "Please Enter Valid Email"),
            # Invalid email format
            ("", "tonyboniee@gmail.com", "9047864060", "Ranees@12345", "Please Enter Name"),
            # Password too short
            ("arkranees", "", "9047864060", "Ranees@12345", "Please Enter Valid Email"),
            # Passwords do not match
            ("arkranees", "tonyboniee@gmail.com", "9047864060", "", "Please Enter Password"),
            # All fields empty
            ("arkranees", "tonyboniee@gmail.com", "9047864060", "ranees0123", "Password must contain a small case "
                                                                              "capital case  a number and a symbol"),
            # Email field empty
            ("a!@#$%1", "tonyboniee@gmail.com", "9047864060", "Ranees@12345", "User mobile or email already exists"),
            # Password field empty
        ]
    )
    def test_register(self, setup, username, email, phone_number, password, expected_result):
        driver = setup
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.ID, "register-tab").click()
        driver.find_element(By.ID, "Name").clear()
        enter_Name = driver.find_element(By.ID, "Name")
        enter_Name.send_keys(username)
        driver.find_element(By.ID, "email").clear()
        enter_Email = driver.find_element(By.ID, "email")
        enter_Email.send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='Enter phone number']").clear()
        # enter_Phonenumber = driver.find_element(By.XPATH, "//input[@placeholder='Enter phone number']")
        enter_Phonenumber = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter phone "
                                                                                   "number']")))
        enter_Phonenumber.send_keys(phone_number)
        driver.find_element(By.ID, "password").clear()
        enter_Password = driver.find_element(By.ID, "password")
        enter_Password.send_keys(password)
        driver.find_element(By.ID, "registerSubmit").click()

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
