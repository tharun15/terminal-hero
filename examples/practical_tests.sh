#!/bin/bash
# Terminal Hero - Practical Examples
# These are real commands you can run to test Terminal Hero

echo "================================"
echo "Terminal Hero - Practical Tests"
echo "================================"
echo ""

# Verify installation
echo "Step 1: Verify Terminal Hero is installed"
echo "Running: terminal-hero monitor --status"
echo ""
terminal-hero monitor --status 2>/dev/null || echo "[!] Terminal Hero not installed yet"
echo ""

echo "Step 2: Install Terminal Hero monitor"
echo "Running: terminal-hero monitor --install"
terminal-hero monitor --install
echo ""

echo "Step 3: Reload shell"
echo "Running: source ~/.bashrc"
source ~/.bashrc
echo ""

echo "Step 4: Start the monitoring daemon"
echo "Running: terminal-hero monitor --start"
terminal-hero monitor --start
echo ""

echo "================================"
echo "Now Terminal Hero is watching!"
echo "================================"
echo ""

echo "Try these commands to test error detection:"
echo ""

echo "Example 1: Missing Command"
echo "  \$ npm start"
echo "  Expected: Terminal Hero detects 'command not found'"
echo ""

echo "Example 2: Permission Error"
echo "  \$ touch test.sh"
echo "  \$ ./test.sh"
echo "  Expected: Terminal Hero suggests 'chmod +x test.sh'"
echo ""

echo "Example 3: Missing Python Package"
echo "  \$ python3 -c 'import nonexistent_package'"
echo "  Expected: Terminal Hero suggests installing the package"
echo ""

echo "Example 4: Port Already in Use"
echo "  \$ python3 -c 'import socket; s = socket.socket(); s.bind((\"127.0.0.1\", 8888))'"
echo "  Expected: Terminal Hero detects port conflict"
echo ""

echo "Try running one of these examples now!"
echo ""

echo "When done, check the monitor status:"
echo "  terminal-hero monitor --status"
echo ""

echo "To see what Terminal Hero learned:"
echo "  terminal-hero monitor --stats"
echo ""
