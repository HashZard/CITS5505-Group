import subprocess
import os
import sys
import time

selenium_dir = os.path.join(os.path.dirname(__file__), "selenium")


test_files = [
    "register_and_login_test.py",
    "search_course_test.py",
    "create_course_test.py",
    "course_rating_and_comment_test.py"

]

for test_file in test_files:
    test_path = os.path.join(selenium_dir, test_file)
    print(f"Running {test_file}...")
    result = subprocess.run([sys.executable, test_path])
    if result.returncode == 0:
        print(f"{test_file} ✅ PASSED\n")
        time.sleep(2)
    else:
        print(f"{test_file} ❌ FAILED\n")
        time.sleep(2)
