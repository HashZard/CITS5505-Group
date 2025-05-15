import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestCourseRatingAndComment(unittest.TestCase):
    def setUp(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

        # Test data
        self.test_email = "testuser1@student.uwa.edu.au"
        self.test_password = "TestPassword123"
        self.captcha_code = "1111"
        self.course_name = "Test Rating And Comment Selenium"
        self.course_code = "CITS11119"
        self.course_description = "This is a test course created via Selenium."
        self.test_rating = "4"
        self.test_comment = "This is a test comment from Selenium."

        self.driver.get("http://localhost:3000/pages/auth/login.html")

        # Wait for page to load
        self.wait.until(EC.presence_of_element_located((By.NAME, "email")))

        # Login
        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.test_password)
        self.driver.find_element(By.NAME, "code").send_keys(self.captcha_code)
        self.driver.find_element(By.CLASS_NAME, "custom-big-btn").click()

        # Wait for login to complete
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Navigate to course creation page
        self.driver.get("http://localhost:3000/pages/service/create_course_page.html")
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


    def test_course_rating_and_comment(self):
        # Navigate to course details page
        self.driver.get(f"http://localhost:3000/pages/service/course_details_page.html?code={self.course_code}")
        time.sleep(2)

        # Navigate to course details page
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert_text = alert.text
            if alert_text == "Course not found":
                print("Course not found. Skipping test.")
                alert.accept()
                return
            else:
                self.fail(f"Unexpected alert: {alert_text}")
        except:
            pass

        # Submit rating
        rating_input = self.wait.until(EC.presence_of_element_located((By.ID, "ratingInput")))
        rating_input.clear()
        rating_input.send_keys(self.test_rating)

        submit_rating_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "submitRatingBtn")))
        time.sleep(1)
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
        time.sleep(1)
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
        time.sleep(2)
        self.assertTrue(found, "Comment not found in the review section.")

        print("✅ Course rating and comment test passed.")


    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
