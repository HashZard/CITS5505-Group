import unittest
import os
import sys

# Get test directory path
current_dir = os.path.dirname(os.path.abspath(__file__))
selenium_dir = os.path.join(current_dir, "selenium")

def discover_and_run_tests():
    """Discover and run all tests"""
    # Use unittest's TestLoader to automatically discover tests
    loader = unittest.TestLoader()
    suite = loader.discover(selenium_dir, pattern="*.py")
    
    # Run tests
    print("Starting Selenium tests...")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Print test result summary
    print("\nTEST RESULTS SUMMARY:")
    print(f"✅ Tests Run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"❌ Errors: {len(result.errors)}")
    
    # Show failed tests
    if result.failures:
        print("\nFailed tests:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    # Show tests with errors
    if result.errors:
        print("\nErrors in tests:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(discover_and_run_tests())
