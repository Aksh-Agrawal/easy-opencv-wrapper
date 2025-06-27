"""
Test runner for Easy OpenCV package.
Executes all tests and reports results.
"""

import os
import sys
import unittest
import importlib

def run_all_tests():
    """Run all tests and return number of failures"""
    # Get the directory where this script is located
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load test modules
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Find all test files
    test_files = [f for f in os.listdir(test_dir) 
                 if f.startswith('test_') and f.endswith('.py')]
    
    if not test_files:
        print("No test files found. Make sure test files start with 'test_' and end with '.py'.")
        return 0
    
    # Add all tests to the suite
    for test_file in sorted(test_files):
        module_name = test_file[:-3]  # Remove .py
        try:
            # Import the module from the current directory
            module_path = f"tests.{module_name}"
            module = importlib.import_module(module_path)
            
            # Add tests from this module
            tests = loader.loadTestsFromModule(module)
            suite.addTests(tests)
            
            print(f"Loaded tests from {module_name}")
        except ImportError as e:
            print(f"Error importing {module_name}: {e}")
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) + len(result.errors)

if __name__ == "__main__":
    print("=" * 70)
    print(f"Running Easy OpenCV Test Suite")
    print("=" * 70)
    
    failures = run_all_tests()
    
    print("\n" + "=" * 70)
    if failures == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ {failures} tests failed.")
    print("=" * 70)
    
    # Return the number of failures as exit code
    sys.exit(failures)
