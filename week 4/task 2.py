from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://your-test-login-page.com")

# Test Case 1: Invalid Credentials
driver.find_element(By.ID, "username").send_keys("wrong_user")
driver.find_element(By.ID, "password").send_keys("wrong_pass")
driver.find_element(By.ID, "login-btn").click()
time.sleep(2)
# Check for error message
error_message = driver.find_element(By.CLASS_NAME, "error").text
assert "Invalid credentials" in error_message

# Test Case 2: Valid Credentials
driver.find_element(By.ID, "username").clear()
driver.find_element(By.ID, "username").send_keys("correct_user")
driver.find_element(By.ID, "password").clear()
driver.find_element(By.ID, "password").send_keys("correct_pass")
driver.find_element(By.ID, "login-btn").click()
time.sleep(2)
# Check for successful redirect
assert "dashboard" in driver.current_url

driver.quit()