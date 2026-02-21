'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Generate .mcp.json.example from manifest MCP recommendations.
 * On Windows, transforms npx command to cmd /c npx for compatibility.
 */
function generateMcpExample(manifest, targetDir) {
  const mcps = manifest.mcps && manifest.mcps.recommended;
  if (!mcps || mcps.length === 0) return false;

  const isWindows = os.platform() === 'win32';
  const servers = {};

  for (const mcp of mcps) {
    let command = mcp.command;
    let args = [...mcp.args];

    // Windows: npx is a shell script, not an .exe — wrap with cmd
    if (isWindows && command === 'npx') {
      command = 'cmd';
      args = ['/c', 'npx', ...args];
    }

    const entry = { command, args };
    if (mcp.purpose) {
      entry._comment = `${mcp.purpose}${mcp.tokens ? ` (${mcp.tokens} tokens)` : ''}`;
    }

    servers[mcp.name] = entry;
  }

  const config = {
    _instructions: 'To enable MCPs: cp .mcp.json.example .mcp.json',
    mcpServers: servers,
  };

  const destPath = path.join(targetDir, '.mcp.json.example');
  fs.writeFileSync(destPath, JSON.stringify(config, null, 2) + '\n', 'utf8');
  return true;
}

module.exports = { generateMcpExample };
