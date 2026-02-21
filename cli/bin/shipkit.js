#!/usr/bin/env node
'use strict';

// Node version check
const [major] = process.versions.node.split('.').map(Number);
if (major < 18) {
  console.error('Shipkit requires Node.js 18 or later. Current: ' + process.version);
  process.exit(1);
}

const { run } = require('../src/index');
run(process.argv.slice(2)).catch(err => {
  console.error(err.message || err);
  process.exit(1);
});
