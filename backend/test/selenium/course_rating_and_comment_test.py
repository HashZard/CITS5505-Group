from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def course_rating_and_comment_test():
    test_email = "testuser1@student.uwa.edu.au"
    test_password = "TestPassword123"
    captcha_code = "1111"

    course_code = "CITS9999"
    test_rating = "4"
    test_comment = "This is a test comment from Selenium."

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    # Log in
    driver.get("http://localhost:3000/pages/auth/login.html")
    driver.find_element(By.NAME, "email").send_keys(test_email)
    driver.find_element(By.NAME, "password").send_keys(test_password)
    driver.find_element(By.NAME, "code").send_keys(captcha_code)
    driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
    time.sleep(2)

    # Navigate to course details page
    driver.get(f"http://localhost:3000/pages/service/course_details_page.html?code={course_code}")

    # Submit rating
    wait.until(EC.presence_of_element_located((By.ID, "ratingInput")))
    driver.find_element(By.ID, "ratingInput").clear()
    driver.find_element(By.ID, "ratingInput").send_keys(test_rating)
    time.sleep(2)
    driver.find_element(By.ID, "submitRatingBtn").click()

    # Handle rating alert
    alert = wait.until(EC.alert_is_present())
    assert alert.text == "Rating submitted!", f"Unexpected alert message: {alert.text}"
    time.sleep(1)
    alert.accept()

    # Submit comment
    driver.find_element(By.ID, "reviewContent").clear()
    driver.find_element(By.ID, "reviewContent").send_keys(test_comment)
    time.sleep(2)
    driver.find_element(By.ID, "submitReviewBtn").click()

    # Handle comment alert
    alert = wait.until(EC.alert_is_present())
    assert alert.text == "Your comment was submitted!", f"Unexpected alert message: {alert.text}"
    time.sleep(1)
    alert.accept()

    # Wait for review section to load
    review_section = wait.until(EC.presence_of_element_located((By.ID, "reviewSection")))
    comment_paragraphs = review_section.find_elements(By.CLASS_NAME, "typography-default")

    # Check if any of the paragraphs contain the test comment
    found = any(test_comment in p.text for p in comment_paragraphs)
    assert found, "Comment not found in the review section."
    time.sleep(2)

    print("✅ Course rating and comment test passed.")
    driver.quit()


if __name__ == "__main__":
    course_rating_and_comment_test()
