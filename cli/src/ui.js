'use strict';

const os = require('os');

function supportsUnicode() {
  if (os.platform() === 'win32') {
    return !!(process.env.WT_SESSION || process.env.TERM_PROGRAM);
  }
  return true;
}

const unicode = supportsUnicode();

const symbols = {
  check: unicode ? '\u2713' : '+',
  cross: unicode ? '\u2717' : 'x',
  warn: unicode ? '\u26A0' : '!',
  arrow: unicode ? '\u2192' : '->',
  bullet: unicode ? '\u2022' : '*',
};

const colors = {
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  reset: '\x1b[0m',
  green: '\x1b[0;32m',
  yellow: '\x1b[1;33m',
  cyan: '\x1b[0;36m',
  red: '\x1b[0;31m',
  magenta: '\x1b[1;35m',
  brightGreen: '\x1b[1;32m',
  brightCyan: '\x1b[1;36m',
};

function success(msg) {
  console.log(`  ${colors.green}${symbols.check}${colors.reset} ${msg}`);
}

function info(msg) {
  console.log(`  ${colors.cyan}${symbols.arrow}${colors.reset} ${msg}`);
}

function warning(msg) {
  console.log(`  ${colors.yellow}${symbols.warn}${colors.reset} ${msg}`);
}

function error(msg) {
  console.log(`  ${colors.red}${symbols.cross}${colors.reset} ${msg}`);
}

function bullet(msg) {
  console.log(`  ${colors.dim}${symbols.bullet}${colors.reset} ${msg}`);
}

function section(title) {
  console.log(`\n${colors.magenta}${'='.repeat(60)}${colors.reset}`);
  console.log(`${colors.magenta}  ${title}${colors.reset}`);
  console.log(`${colors.magenta}${'='.repeat(60)}${colors.reset}\n`);
}

function logo(version) {
  console.log(`
${colors.brightCyan}  ____  _     _       _  ___ _
 / ___|| |__ (_)_ __ | |/ (_) |_
 \\___ \\| '_ \\| | '_ \\| ' /| | __|
  ___) | | | | | |_) | . \\| | |_
 |____/|_| |_|_| .__/|_|\\_\\_|\\__|
               |_|${colors.reset}  ${colors.dim}v${version}${colors.reset}
`);
}

module.exports = { symbols, colors, success, info, warning, error, bullet, section, logo };
