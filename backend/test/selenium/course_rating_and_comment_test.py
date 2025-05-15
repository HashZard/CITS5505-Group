import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestCourseRatingAndComment(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")  # Enable headless mode
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test data
        self.test_email = "testuser1@student.uwa.edu.au"
        self.test_password = "TestPassword123"
        self.captcha_code = "1111"
        self.course_code = "CITS9999"
        self.test_rating = "4"
        self.test_comment = "This is a test comment from Selenium."

    def test_course_rating_and_comment(self):
        # Login process
        self.driver.get("http://localhost:3000/pages/auth/login.html")
        self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        
        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "code").send_keys(self.captcha_code)
        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
        
        # Wait for login to complete
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Navigate to course details page
        self.driver.get(f"http://localhost:3000/pages/service/course_details_page.html?code={self.course_code}")

        # Submit rating
        rating_input = self.wait.until(EC.presence_of_element_located((By.ID, "ratingInput")))
        rating_input.clear()
        rating_input.send_keys(self.test_rating)
        
        submit_rating_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "submitRatingBtn")))
        submit_rating_btn.click()

        # Handle rating alert
        alert = self.wait.until(EC.alert_is_present())
        self.assertEqual(alert.text, "Rating submitted!", 
                         f"Unexpected alert message: {alert.text}")
        alert.accept()

        # Submit comment
        review_input = self.wait.until(EC.presence_of_element_located((By.ID, "reviewContent")))
        review_input.clear()
        review_input.send_keys(self.test_comment)
        
        submit_review_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "submitReviewBtn")))
        submit_review_btn.click()

        # Handle comment alert
        alert = self.wait.until(EC.alert_is_present())
        self.assertEqual(alert.text, "Your comment was submitted!", 
                         f"Unexpected alert message: {alert.text}")
        alert.accept()

        # Wait for review section to load
        review_section = self.wait.until(EC.presence_of_element_located((By.ID, "reviewSection")))
        
        # Wait for new comment to appear
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "reviewSection"), self.test_comment))
        
        # Verify comment content
        comment_paragraphs = review_section.find_elements(By.CLASS_NAME, "typography-default")
        found = any(self.test_comment in p.text for p in comment_paragraphs)
        self.assertTrue(found, "Comment not found in the review section.")

        print("✅ Course rating and comment test passed.")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()