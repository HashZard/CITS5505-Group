# selenium/create_course_test.py
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestCourseCreation(unittest.TestCase):
    def setUp(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test data
        self.test_email = "admin@example.com"
        self.test_password = "admin2025"
        self.captcha_code = "1111"
        self.course_name = "Test Course Selenium"
        self.course_code = "CITS11112"
        self.course_description = "This is a test course created via Selenium."

        # Login
        self.driver.get("http://localhost:3000/pages/auth/login.html")
        time.sleep(1)

        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "code").send_keys(self.captcha_code)
        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()

        # Wait for login to complete
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def test_create_course(self):

        # Navigate to course creation page
        self.driver.get("http://localhost:3000/pages/service/create_course_page.html")
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        # Fill in the form
        def fill_input_by_label(label_text, value):
            label = self.driver.find_element(By.XPATH, f"//label[text()='{label_text}']")
            input_el = label.find_element(By.XPATH, "following-sibling::input | following-sibling::textarea")
            input_el.clear()
            input_el.send_keys(value)

        fill_input_by_label("Course Name", self.course_name)
        fill_input_by_label("Course Code", self.course_code)
        fill_input_by_label("Course Description", self.course_description)

        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()

        # Handle alert dialog
        time.sleep(2)
        alert = self.wait.until(EC.alert_is_present())
        alert_text = alert.text
        time.sleep(1)
        if "success" in alert_text.lower():
            self.assertIn("success", alert_text.lower(), "Alert should indicate success")
        elif "failed" in alert_text.lower():
            self.assertIn("failed to create course", alert_text.lower(),
                          "Alert should indicate failure if course already exists")
        else:
            self.fail(f"Unexpected alert message: {alert_text}")
        alert.accept()
        time.sleep(2)

        # Search for the created course
        self.wait.until(EC.presence_of_element_located((By.ID, "header-search-input")))
        search_input = self.driver.find_element(By.ID, "header-search-input")
        search_input.clear()
        search_input.send_keys(self.course_code)
        self.driver.find_element(By.ID, "header-search-btn").click()

        # Verify search results page
        time.sleep(2)
        self.wait.until(EC.url_contains(f"course_search_result.html?keyword={self.course_code}"))

        # Verify search results contain the created course
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.ID, "course-list")))
        tag_span = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[@class='tag' and text()='{self.course_code}']"))
        )
        time.sleep(2)
        self.assertIsNotNone(tag_span, f"Course with code {self.course_code} should be in search results")

        print("✅ Course creation test passed.")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
