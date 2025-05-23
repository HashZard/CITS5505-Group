import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestCourseSearch(unittest.TestCase):
    def setUp(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test data
        self.test_email = "admin@example.com"
        self.test_password = "admin2025"
        self.captcha_code = "1111"
        self.search_keyword = "CITS"

        # Login
        self.driver.get("http://localhost:3000/pages/auth/login.html")
        time.sleep(1)

        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "code").send_keys(self.captcha_code)
        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()

        # Wait for login to complete
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.ID, "header-search-input")))

    def test_course_search(self):

        # Perform search
        search_input = self.driver.find_element(By.ID, "header-search-input")
        search_input.send_keys(self.search_keyword)
        time.sleep(1)
        self.driver.find_element(By.ID, "header-search-btn").click()

        # Verify search results page
        time.sleep(2)
        self.wait.until(EC.url_contains(f"course_search_result.html?keyword={self.search_keyword}"))

        # Verify search results list exists
        course_list = self.wait.until(EC.presence_of_element_located((By.ID, "course-list")))
        time.sleep(2)
        self.assertIsNotNone(course_list, "Course list should be present")

        # Verify search results contain the keyword
        page_source = self.driver.page_source
        self.assertIn(self.search_keyword, page_source, 
                     f"Search results should contain the keyword '{self.search_keyword}'")

        print("✅ Course search test passed!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
