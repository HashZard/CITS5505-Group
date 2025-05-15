# selenium/create_course_test.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def create_course_test():
    test_email = "testuser1@student.uwa.edu.au"
    test_password = "TestPassword123"
    captcha_code = "1111"

    course_name = "Test Course Selenium"
    course_code = "CITS9999"
    course_description = "This is a test course created via Selenium."

    driver = webdriver.Chrome()
    driver.get("http://localhost:3000/pages/auth/login.html")
    time.sleep(1)

    # Log in
    driver.find_element(By.NAME, "email").send_keys(test_email)
    driver.find_element(By.NAME, "password").send_keys(test_password)
    driver.find_element(By.NAME, "code").send_keys(captcha_code)
    driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
    time.sleep(2)

    # Navigate to course creation page
    driver.get("http://localhost:3000/pages/service/create_course_page.html")
    time.sleep(2)

    # Fill in form
    def fill_input_by_label(label_text, value):
        label = driver.find_element(By.XPATH, f"//label[text()='{label_text}']")
        input_el = label.find_element(By.XPATH, "following-sibling::input | following-sibling::textarea")
        input_el.clear()
        input_el.send_keys(value)

    fill_input_by_label("Course Name", course_name)
    fill_input_by_label("Course Code", course_code)
    fill_input_by_label("Course Description", course_description)

    driver.find_element(By.CLASS_NAME, "custom-big-btn").click()

    # Handle alert
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)

    # Search for course
    search_input = driver.find_element(By.ID, "header-search-input")
    search_input.clear()
    search_input.send_keys(course_code)
    driver.find_element(By.ID, "header-search-btn").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains(f"course_search_result.html?keyword={course_code}")
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "course-list"))
    )
    tag_span = driver.find_element(By.XPATH, f"//span[@class='tag' and text()='{course_code}']")
    assert tag_span is not None
    time.sleep(2)

    print("✅ Course creation test passed.")
    driver.quit()


if __name__ == "__main__":
    create_course_test()
