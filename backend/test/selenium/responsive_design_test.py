import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class TestResponsiveDesign(unittest.TestCase):
    def setUp(self):
        options = Options()
        # Note: We don't use headless mode in responsive design tests as we need to test different screen sizes
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        self.sizes = [
            ("Mobile", 375, 667, True),     # Should show hamburger
            ("Tablet", 768, 1024, True),    # Should show hamburger
            ("Desktop", None, None, False)  # Fullscreen - should NOT show hamburger
        ]

    def test_responsive_design(self):
        for mode, width, height, should_show in self.sizes:
            print(f"\n🔎 Testing {mode} mode...")
            if mode == "Desktop":
                self.driver.maximize_window()
            else:
                self.driver.set_window_size(width, height)

            self.driver.get("http://localhost:3000")

            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                if mode != "Desktop":  # On small screens, hamburger menu button should be visible
                    hamburger = self.driver.find_element(By.CLASS_NAME, "flex")
                    self.assertTrue(hamburger.is_displayed(), f"{mode}: Hamburger should be visible")
                    print(f"✅ {mode}: Hamburger menu is visible")
                else:  # In desktop mode, full menu should be visible instead of hamburger
                    nav_links = self.driver.find_elements(By.CLASS_NAME, "nav-link")
                    self.assertTrue(len(nav_links) > 0 and nav_links[0].is_displayed(), 
                                   f"{mode}: Navigation links should be visible")
                    print(f"✅ {mode}: Full navigation menu is visible")
            except Exception as e:
                self.fail(f"{mode} test failed: {e}")

        print("✅ Responsive design test passed!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    unittest.main()
