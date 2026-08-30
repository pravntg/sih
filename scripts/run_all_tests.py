"""
Project ORCA — End-to-End System Test Runner
Validates Backend Services, API Contracts, Provenance Enforcement, and Design System Compliance.
"""
import subprocess
import sys
import time
import os

def run_command(cmd, desc):
    print("\n" + "="*56)
    print(f">> RUNNING: {desc}")
    print(f"   Command: {cmd}")
    print("="*56)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[FAIL] FAILED: {desc}")
        return False
    print(f"[PASS] PASSED: {desc}")
    return True

def main():
    start_time = time.time()
    results = []

    # 1. Frontend Strict Palette Verification
    results.append(run_command(
        "node frontend/scripts/verify-palette.js",
        "Frontend Palette & Strict 5-Color UI Rule Compliance"
    ))

    # 2. Backend Pytest & Coverage
    results.append(run_command(
        "py -m pytest backend/tests -v --cov=backend/src",
        "Backend Unit & Integration Tests (Target >= 70% Coverage)"
    ))

    # 3. Ops Cycle Monitor
    results.append(run_command(
        "py ops/cycle-monitor/monitor.py",
        "120-Minute Developer-Manager Dev Loop Monitor"
    ))

    # 4. Standalone Contract & Domain Tests
    results.append(run_command(
        "py backend/tests/run_unittests.py",
        "Geospatial PFZ & Chat Advisory Contract Verification"
    ))

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "="*56)
    print("                 TEST SUMMARY REPORT                    ")
    print("="*56)
    passed_count = sum(1 for r in results if r)
    total_count = len(results)
    print(f"Total Suites : {total_count}")
    print(f"Passed       : {passed_count}")
    print(f"Failed       : {total_count - passed_count}")
    print(f"Duration     : {elapsed}s")
    
    if passed_count == total_count:
        print("STATUS       : [SUCCESS] ALL TEST SUITES PASSED (100% GREEN)")
    else:
        print("STATUS       : [FAILURE] SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
