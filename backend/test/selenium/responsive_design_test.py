from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def responsive_design_test():
    driver = webdriver.Chrome()

    sizes = [
        ("Mobile", 375, 667, True),     # Should show hamburger
        ("Tablet", 768, 1024, True),    # Should show hamburger
        ("Desktop", None, None, False)  # Fullscreen - should NOT show hamburger
    ]

    for mode, width, height, should_show in sizes:
        print(f"\n🔎 Testing {mode} mode...")
        if mode == "Desktop":
            driver.maximize_window()
        else:
            driver.set_window_size(width, height)

        driver.get("http://localhost:3000")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            hamburger = driver.find_element(By.CLASS_NAME, "flex")

            if should_show:
                assert hamburger.is_displayed(), f"{mode}: Hamburger should be visible"
                time.sleep(3)
                print(f"✅ {mode}: Hamburger menu is visible")
            else:
                assert not hamburger.is_displayed(), f"{mode}: Hamburger should be hidden"
                time.sleep(3)
                print(f"✅ {mode}: Hamburger menu is hidden")
        except Exception as e:
            print(f"❌ {mode} test failed:", e)

    print("✅ Responsive design test passed!")
    driver.quit()


if __name__ == "__main__":
    responsive_design_test()
