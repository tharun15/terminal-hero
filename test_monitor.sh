#!/bin/bash
# Terminal Hero - Test Script
# Run this to test the autonomous monitoring system

echo "================================================"
echo "  Terminal Hero - Autonomous Monitor Test"
echo "================================================"
echo ""

# Test 1: command_not_found
echo "Test 1: command_not_found error"
echo "Running: npm start (when npm not installed)"
echo "Expected: Terminal Hero detects and suggests npm installation"
echo ""
echo "Try it yourself:"
echo "  $ npm start"
echo ""
read -p "Press Enter to continue..."
echo ""

# Test 2: permission_denied
echo "Test 2: permission_denied error"
echo "Running: ./script.sh (without execute permission)"
echo "Expected: Terminal Hero detects and suggests chmod +x"
echo ""
echo "Try it yourself:"
echo "  $ touch test_script.sh"
echo "  $ ./test_script.sh"
echo ""
read -p "Press Enter to continue..."
echo ""

# Test 3: missing_dependency
echo "Test 3: missing_dependency error"
echo "Running: python -c 'import requests' (when requests not installed)"
echo "Expected: Terminal Hero detects and suggests pip install"
echo ""
echo "Try it yourself:"
echo "  $ python3 -c 'import numpy'"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "================================================"
echo "  Test Results Summary"
echo "================================================"
echo ""
echo "If Terminal Hero is running:"
echo "  ✓ Each error was detected automatically"
echo "  ✓ Error type was identified correctly"
echo "  ✓ Confidence score was calculated"
echo "  ✓ Suggestion or auto-fix was offered"
echo ""
echo "Check monitor status:"
echo "  terminal-hero monitor --status"
echo ""
echo "View learning progress:"
echo "  terminal-hero monitor --stats"
echo ""
