import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestRegisterAndLogin(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")  # 启用headless模式
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test data
        self.test_email = "testuser1@student.uwa.edu.au"
        self.test_password = "TestPassword123"
        self.captcha_code = "1111"

    def test_register_and_login(self):
        # Step 1: Go to registration page
        self.driver.get("http://localhost:3000/pages/auth/register.html")
        
        # Step 2: Fill in registration form
        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "confirm_password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "code").send_keys(self.captcha_code)
        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
        
        # Wait for alert and accept it
        alert = self.wait.until(EC.alert_is_present())
        print(f"Alert says: {alert.text}")  # Optional: log alert message
        alert.accept()

        # Step 3: Go to login page
        self.driver.get("http://localhost:3000/pages/auth/login.html")
        
        # Step 4: Fill in login form
        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "code").send_keys(self.captcha_code)
        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
        
        # Step 5: Verify redirection to homepage
        self.wait.until(EC.url_to_be("http://localhost:3000/index.html"))
        self.assertEqual(self.driver.current_url, "http://localhost:3000/index.html", 
                         "❌ Did not redirect to homepage")

        # Step 6: Go to profile page and check email
        self.driver.get("http://localhost:3000/pages/service/profile.html")
        
        user_email_element = self.wait.until(EC.presence_of_element_located((By.ID, "userEmail")))
        self.assertEqual(user_email_element.text, self.test_email, 
                         "❌ User email not found or does not match")

        print("✅ Registration and login test passed!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
