from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_course_search():
    test_email = "testuser1@student.uwa.edu.au"
    test_password = "TestPassword123"
    captcha_code = "1111"

    driver = webdriver.Chrome()
    driver.get("http://localhost:3000")
    time.sleep(2)

    driver.find_element(By.NAME, "email").send_keys(test_email)
    driver.find_element(By.NAME, "password").send_keys(test_password)
    driver.find_element(By.NAME, "code").send_keys(captcha_code)
    driver.find_element(By.CLASS_NAME, "custom-big-btn").click()
    time.sleep(2)

    search_input = driver.find_element(By.ID, "header-search-input")
    search_input.send_keys("CITS")
    driver.find_element(By.ID, "header-search-btn").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("course_search_result.html?keyword=CITS")
    )

    course_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "course-list"))
    )
    assert course_list is not None
    time.sleep(2)

    print("✅ Course search test passed!")
    driver.quit()


if __name__ == "__main__":
    test_course_search()
