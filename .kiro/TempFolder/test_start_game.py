#!/usr/bin/env python3
"""Test start_game tool"""

import json
import subprocess
import sys
import time

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

print("\n=== Testing start_game ===")
print("This will build and launch Godot...")

request = {
    "method": "tools/call",
    "params": {
        "name": "start_game",
        "arguments": {}
    }
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()

print("Waiting for response...")
response_line = process.stdout.readline()
response = json.loads(response_line)

if response.get('isError'):
    print(f"\n❌ Error: {response['content'][0]['text']}")
else:
    print(f"\n✅ Success!")
    print(response['content'][0]['text'])
    print("\nGodot should now be running. Check if the game window appeared.")
    print("The MCP server inside Godot should be listening on port 8765.")

# Keep bridge running for a bit
print("\nWaiting 5 seconds...")
time.sleep(5)

# Test if we can connect to Godot's MCP server
print("\n=== Testing connection to Godot MCP Server ===")
request = {
    "method": "tools/call",
    "params": {
        "name": "get_scene_tree",
        "arguments": {}
    }
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()

response_line = process.stdout.readline()
response = json.loads(response_line)

if response.get('isError'):
    print(f"❌ Cannot connect to Godot: {response['content'][0]['text']}")
    print("Make sure Godot is running and MCP server is started.")
else:
    print(f"✅ Connected to Godot!")
    print("Scene tree data received.")

print("\n=== Test completed ===")
print("Press Ctrl+C to stop, or close Godot manually.")

# Cleanup
process.terminate()
process.wait()
