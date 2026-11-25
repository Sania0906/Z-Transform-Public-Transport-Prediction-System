"""
Master Automated Test Runner for Z-Transform Public Transport Arrival Prediction System.
Runs all unit and integration test suites and compiles an academic verification report.
"""

import unittest
import sys
import os
import time

# Ensure project root in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.test_database import TestDatabaseManager
from tests.test_data_pipeline import TestDataPipeline
from tests.test_z_transform import TestZTransformEngine
from tests.test_prediction import TestPredictionEngine

def run_test_suite():
    print("=" * 80)
    print("  Z-TRANSFORM PUBLIC TRANSPORT ARRIVAL PREDICTION SYSTEM - TEST SUITE")
    print("=" * 80)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]} | Workspace: {PROJECT_ROOT}\n")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suites = [
        ("Database & Schema Operations", loader.loadTestsFromTestCase(TestDatabaseManager)),
        ("Module 1: Data Pipeline & Preprocessing", loader.loadTestsFromTestCase(TestDataPipeline)),
        ("Module 2: Z-Transform Engine & Pole-Zero", loader.loadTestsFromTestCase(TestZTransformEngine)),
        ("Module 3: Prediction & Passenger Dashboard", loader.loadTestsFromTestCase(TestPredictionEngine))
    ]

    for name, s in suites:
        print(f"Loading {name} ({s.countTestCases()} test cases)...")
        suite.addTests(s)

    print("-" * 80)
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start_time
    print("-" * 80)

    print("\n" + "=" * 80)
    print("  ACADEMIC TEST VERIFICATION SUMMARY REPORT")
    print("=" * 80)
    print(f"Total Test Cases Executed : {result.testsRun}")
    print(f"Passed                    : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures                  : {len(result.failures)}")
    print(f"Errors                    : {len(result.errors)}")
    print(f"Execution Duration        : {elapsed:.3f} seconds")
    print(f"System Verification Status: {'ALL TESTS PASSED (100% SUCCESS)' if result.wasSuccessful() else 'TEST FAILURES DETECTED'}")
    print("=" * 80 + "\n")

    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_test_suite())
