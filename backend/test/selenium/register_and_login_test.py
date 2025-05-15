import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def register_and_login_test():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Test data
    test_email = "testuser1@student.uwa.edu.au"
    test_password = "TestPassword123"
    captcha_code = "1111"

    # Step 1: Go to registration page
    driver.get("http://localhost:3000/pages/auth/register.html")
    time.sleep(1)

    # Step 2: Fill in registration form
    driver.find_element(By.NAME, "email").send_keys(test_email)
    driver.find_element(By.NAME, "password").send_keys(test_password)
    driver.find_element(By.NAME, "confirm_password").send_keys(test_password)
    driver.find_element(By.NAME, "code").send_keys(captcha_code)
    driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
    time.sleep(2)  # wait for registration to complete

    # Wait for alert and accept it
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"Alert says: {alert.text}")  # Optional: log alert message
    alert.accept()

    # Step 3: Go to login page
    driver.get("http://localhost:3000/pages/auth/login.html")
    time.sleep(1)

    # Step 4: Fill in login form
    driver.find_element(By.NAME, "email").send_keys(test_email)
    driver.find_element(By.NAME, "password").send_keys(test_password)
    driver.find_element(By.NAME, "code").send_keys(captcha_code)
    driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
    time.sleep(2)  # wait for login

    # Step 5: Verify redirection to homepage
    assert driver.current_url == "http://localhost:3000/index.html", "❌ Did not redirect to homepage"

    # Step 6: Go to profile page and check email
    driver.get("http://localhost:3000/pages/service/profile.html")
    time.sleep(2)

    user_email_element = driver.find_element(By.ID, "userEmail")
    assert user_email_element.text == test_email, "❌ User email not found or does not match"

    print("✅ Registration and login test passed!")

    # Clean up
    driver.quit()


if __name__ == "__main__":
    register_and_login_test()
