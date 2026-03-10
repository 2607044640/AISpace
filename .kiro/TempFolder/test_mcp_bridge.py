#!/usr/bin/env python3
"""Test Godot MCP Bridge"""

import json
import subprocess
import sys

# Start the bridge
bridge_path = r"C:\Godot\new-game-project-test-godot\.kiro\scripts\godot_mcp_bridge.py"

print("Starting MCP bridge...")
process = subprocess.Popen(
    ["python", bridge_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Test 1: List tools
print("\n=== Test 1: List Tools ===")
request = {
    "method": "tools/list",
    "params": {}
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()

response_line = process.stdout.readline()
response = json.loads(response_line)
print(f"Available tools: {len(response.get('tools', []))}")
for tool in response.get('tools', []):
    print(f"  - {tool['name']}: {tool['description']}")

# Test 2: Build project
print("\n=== Test 2: Build Project ===")
request = {
    "method": "tools/call",
    "params": {
        "name": "build_project",
        "arguments": {}
    }
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()

response_line = process.stdout.readline()
response = json.loads(response_line)
if response.get('isError'):
    print(f"Error: {response['content'][0]['text']}")
else:
    print(f"Success: {response['content'][0]['text'][:200]}...")

# Test 3: Get logs
print("\n=== Test 3: Get Logs (last 10 lines) ===")
request = {
    "method": "tools/call",
    "params": {
        "name": "get_logs",
        "arguments": {"lines": 10}
    }
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()

response_line = process.stdout.readline()
response = json.loads(response_line)
if response.get('isError'):
    print(f"Error: {response['content'][0]['text']}")
else:
    logs = response['content'][0]['text']
    print(f"Retrieved logs:\n{logs[:300]}...")

print("\n=== All tests completed ===")

# Cleanup
process.terminate()
process.wait()
