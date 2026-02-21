'use strict';

const fs = require('fs');
const path = require('path');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function copyFile(src, dest) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

function copyDir(src, dest) {
  ensureDir(dest);
  fs.cpSync(src, dest, { recursive: true });
}

function copyFileIfNotExists(src, dest) {
  if (fs.existsSync(dest)) return false;
  copyFile(src, dest);
  return true;
}

function makeExecutable(filePath) {
  if (process.platform !== 'win32') {
    try {
      fs.chmodSync(filePath, 0o755);
    } catch (_) {
      // ignore permission errors
    }
  }
}

module.exports = { ensureDir, copyFile, copyDir, copyFileIfNotExists, makeExecutable };
