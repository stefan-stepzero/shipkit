# Shipkit Installers

## Recommended: npx CLI

```bash
cd your-project
npx shipkit-dev init        # Fresh install
npx shipkit-dev update      # Update existing
```

No clone needed. Zero dependencies beyond Node.js 18+. Add `-y` for non-interactive mode.

---

## Alternative Installers

This directory contains alternative installation scripts for environments without Node.js.

### Python Installer (Cross-Platform)
**File:** `install.py`

Works on:
- ✅ Windows, macOS, Linux
- ✅ Only requires Python 3.6+
- ✅ No other dependencies

**Command Line Usage:**
```bash
# Interactive mode (requires local repo)
python install.py

# Download from GitHub and install (no local repo needed)
python install.py --from-github --target /path/to/project

# Install to specific directory
python install.py --target /path/to/project

# Non-interactive mode (all defaults)
python install.py -y --all-skills --all-agents --no-mcps --target /path/to/project

# Custom profile and language
python install.py --profile minimal --language python --target /path/to/project
```

**GitHub Installation (no local clone needed):**
```bash
# Download and install from main branch
python install.py --from-github --target /path/to/project

# Use a specific branch
python install.py --from-github --branch develop --target /path/to/project

# Use a different repo (for forks)
python install.py --from-github --repo myuser/shipkit --target /path/to/project
```

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

---

### PowerShell Installer (Windows Native)
**File:** `install.ps1`

Works on:
- ✅ Windows 10/11 (native PowerShell)
- ✅ No Git required
- ✅ Interactive terminal interface

**Command Line Usage:**
```powershell
cd your-project
..\shipkit\installers\install.ps1
```

**Advanced usage:**
```powershell
# Install to specific directory
.\install.ps1 C:\Projects\MyProject

# Non-interactive mode
.\install.ps1 C:\Projects\MyProject -Yes

# Show help
.\install.ps1 -Help
```

**Execution Policy Note:**
If you get an execution policy error, the batch launcher (`Install-PowerShell.bat`) bypasses this automatically. Or run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Bash Installer (Deprecated)
**File:** `deprecated/install.sh`

> **Note:** Use `npx shipkit-dev init` instead. This installer is no longer maintained.

Works on macOS, Linux, Windows (Git Bash, WSL). Requires a local clone of the repo.

## What Gets Installed

All installation methods create the same structure in your project:

```
your-project/
├── CLAUDE.md                 # Project instructions for Claude
├── .claude/
│   ├── settings.json         # Permissions + hooks
│   ├── skills/               # <!-- sync:skill_count -->37<!-- /sync:skill_count --> skill definitions
│   ├── agents/               # <!-- sync:agent_count -->9<!-- /sync:agent_count --> agent personas
│   ├── rules/                # Framework rules
│   └── hooks/                # Session hooks
└── .shipkit/
    └── [context files]       # Specs, plans, architecture, etc.
```

## Future Installers

Potential additional installation methods:

- **Claude Code plugin** - Native CC plugin distribution
- **Homebrew formula** - `brew install shipkit`
- **VS Code extension** - One-click install from marketplace
