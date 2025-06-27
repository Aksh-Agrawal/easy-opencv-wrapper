"""
Simple script to run an individual test file
Usage: python run_single_test.py <test_file_name>
Example: python run_single_test.py test_image_operations.py
"""

import sys
import os
import unittest
import importlib


def run_single_test(test_file):
    """Run a single test file"""
    # Verify file exists
    if not os.path.exists(os.path.join('tests', test_file)):
        print(f"Error: Test file {test_file} not found in the tests directory")
        return 1
    
    # Get module name (remove .py)
    module_name = test_file[:-3] if test_file.endswith('.py') else test_file
    
    # Run the test
    try:
        # Import the module
        module_path = f"tests.{module_name}"
        module = importlib.import_module(module_path)
        
        # Run the tests in this module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return len(result.failures) + len(result.errors)
    
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_single_test.py <test_file_name>")
        print("Example: python run_single_test.py test_image_operations.py")
        sys.exit(1)
    
    test_file = sys.argv[1]
    print("=" * 70)
    print(f"Running test: {test_file}")
    print("=" * 70)
    
    failures = run_single_test(test_file)
    
    print("\n" + "=" * 70)
    if failures == 0:
        print("✅ Test passed!")
    else:
        print(f"❌ {failures} tests failed.")
    print("=" * 70)
    
    sys.exit(failures)
