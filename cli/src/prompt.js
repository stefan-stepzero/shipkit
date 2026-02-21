'use strict';

const readline = require('readline');
const { colors, symbols } = require('./ui');

function createInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

function ask(rl, question) {
  return new Promise(resolve => {
    rl.question(question, answer => resolve(answer.trim()));
  });
}

async function confirm(rl, prompt, defaultYes = true) {
  const hint = defaultYes ? '[Y/n]' : '[y/N]';
  const answer = await ask(rl, `  ${prompt} ${colors.dim}${hint}${colors.reset} `);
  if (answer === '') return defaultYes;
  return answer.toLowerCase().startsWith('y');
}

async function promptForProfile(rl) {
  console.log(`\n  Available profiles:\n`);
  console.log(`    ${colors.brightCyan}1${colors.reset}  shipkit    ${colors.dim}Full framework (36 skills, 9 agents)${colors.reset}`);
  console.log(`    ${colors.brightCyan}2${colors.reset}  discovery  ${colors.dim}Vision & planning focused${colors.reset}`);
  console.log(`    ${colors.brightCyan}3${colors.reset}  minimal    ${colors.dim}Core workflow only${colors.reset}`);
  console.log();

  const answer = await ask(rl, `  Select profile ${colors.dim}[1]${colors.reset}: `);
  switch (answer) {
    case '2':
    case 'discovery':
      return 'discovery';
    case '3':
    case 'minimal':
      return 'minimal';
    default:
      return 'shipkit';
  }
}

async function promptForSkills(rl, manifest) {
  const optional = manifest.skills.optional;
  const categories = Object.keys(optional);
  const allSkills = [];

  // Build flat indexed list
  for (const cat of categories) {
    for (const skill of optional[cat]) {
      allSkills.push({ ...skill, category: cat, selected: true });
    }
  }

  let done = false;
  while (!done) {
    console.log(`\n  ${colors.bold}Skill Selection${colors.reset} ${colors.dim}(${allSkills.filter(s => s.selected).length}/${allSkills.length} selected)${colors.reset}\n`);

    let idx = 1;
    for (const cat of categories) {
      const catSkills = allSkills.filter(s => s.category === cat);
      console.log(`  ${colors.magenta}${cat}${colors.reset}`);
      for (const skill of catSkills) {
        const marker = skill.selected
          ? `${colors.green}${symbols.check}${colors.reset}`
          : `${colors.dim}-${colors.reset}`;
        console.log(`    ${colors.dim}${String(idx).padStart(2)}${colors.reset} ${marker} ${skill.name.replace('shipkit-', '')}  ${colors.dim}${skill.desc}${colors.reset}`);
        skill._idx = idx;
        idx++;
      }
    }

    console.log(`\n  ${colors.dim}Commands: [numbers] toggle  [a] all  [n] none  [c:Name] toggle category  [Enter] continue${colors.reset}`);
    const answer = await ask(rl, `\n  ${symbols.arrow} `);

    if (answer === '') {
      done = true;
    } else if (answer.toLowerCase() === 'a') {
      allSkills.forEach(s => s.selected = true);
    } else if (answer.toLowerCase() === 'n') {
      allSkills.forEach(s => s.selected = false);
    } else if (answer.toLowerCase().startsWith('c:')) {
      const catName = answer.slice(2).trim().toLowerCase();
      const matches = allSkills.filter(s => s.category.toLowerCase().includes(catName));
      if (matches.length > 0) {
        const allSelected = matches.every(s => s.selected);
        matches.forEach(s => s.selected = !allSelected);
      }
    } else {
      // Toggle individual numbers
      const nums = answer.split(/[\s,]+/).map(Number).filter(n => !isNaN(n));
      for (const num of nums) {
        const skill = allSkills.find(s => s._idx === num);
        if (skill) skill.selected = !skill.selected;
      }
    }
  }

  // Return mandatory + selected optional
  const mandatory = manifest.skills.mandatory || [];
  const selected = allSkills.filter(s => s.selected).map(s => s.name);
  return [...mandatory, ...selected];
}

async function promptForAgents(rl, manifest) {
  const agents = manifest.agents.map(a => ({ ...a, selected: true }));

  let done = false;
  while (!done) {
    console.log(`\n  ${colors.bold}Agent Selection${colors.reset} ${colors.dim}(${agents.filter(a => a.selected).length}/${agents.length} selected)${colors.reset}\n`);

    agents.forEach((agent, i) => {
      const marker = agent.selected
        ? `${colors.green}${symbols.check}${colors.reset}`
        : `${colors.dim}-${colors.reset}`;
      console.log(`    ${colors.dim}${String(i + 1).padStart(2)}${colors.reset} ${marker} ${agent.name.replace('shipkit-', '').replace('-agent', '')}  ${colors.dim}${agent.desc}${colors.reset}`);
    });

    console.log(`\n  ${colors.dim}Commands: [numbers] toggle  [a] all  [n] none  [Enter] continue${colors.reset}`);
    const answer = await ask(rl, `\n  ${symbols.arrow} `);

    if (answer === '') {
      done = true;
    } else if (answer.toLowerCase() === 'a') {
      agents.forEach(a => a.selected = true);
    } else if (answer.toLowerCase() === 'n') {
      agents.forEach(a => a.selected = false);
    } else {
      const nums = answer.split(/[\s,]+/).map(Number).filter(n => !isNaN(n));
      for (const num of nums) {
        if (num >= 1 && num <= agents.length) {
          agents[num - 1].selected = !agents[num - 1].selected;
        }
      }
    }
  }

  return agents.filter(a => a.selected).map(a => a.name);
}

async function promptForClaudeMdAction(rl, targetDir) {
  const fs = require('fs');
  const path = require('path');
  const exists = fs.existsSync(path.join(targetDir, 'CLAUDE.md'));

  if (!exists) return 'install';

  console.log(`\n  ${colors.yellow}CLAUDE.md already exists.${colors.reset}\n`);
  console.log(`    ${colors.brightCyan}1${colors.reset}  merge      ${colors.dim}Append Shipkit sections to existing file${colors.reset}`);
  console.log(`    ${colors.brightCyan}2${colors.reset}  skip       ${colors.dim}Keep existing file unchanged${colors.reset}`);
  console.log(`    ${colors.brightCyan}3${colors.reset}  overwrite  ${colors.dim}Replace with Shipkit template${colors.reset}`);
  console.log();

  const answer = await ask(rl, `  Select action ${colors.dim}[1]${colors.reset}: `);
  switch (answer) {
    case '2':
    case 'skip':
      return 'skip';
    case '3':
    case 'overwrite':
      return 'overwrite';
    default:
      return 'merge';
  }
}

module.exports = {
  createInterface,
  ask,
  confirm,
  promptForProfile,
  promptForSkills,
  promptForAgents,
  promptForClaudeMdAction,
};
