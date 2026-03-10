import json
import re

# Read the file
with open(r'C:\Users\26070\.kiro\settings\mcp.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove comments
lines = content.split('\n')
cleaned_lines = []
for line in lines:
    # Remove // comments
    if '//' in line:
        line = line[:line.index('//')]
    cleaned_lines.append(line)

cleaned_content = '\n'.join(cleaned_lines)

# Parse JSON
data = json.loads(cleaned_content)

# Move godot-game into mcpServers if it exists outside
if 'godot-game' in data and 'godot-game' not in data.get('mcpServers', {}):
    godot_config = data.pop('godot-game')
    data['mcpServers']['godot-game'] = godot_config
    print("Moved godot-game into mcpServers")

# Write back (without comments)
with open(r'C:\Users\26070\.kiro\settings\mcp.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixed MCP configuration!")
print("\nPlease restart Kiro or reconnect the MCP server from the MCP Server view.")
