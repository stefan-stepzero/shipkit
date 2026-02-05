# Shipkit Installers

This directory contains installation scripts for deploying Shipkit to your projects.

## Available Installers

### 🖱️ Double-Click Installers (Windows - Easiest!)

**Python Version (Recommended):**
- **File:** `Install-Python.bat`
- **Requirements:** Python 3.6+ installed
- **Just double-click** → Follow prompts → Done!

**PowerShell Version:**
- **File:** `Install-PowerShell.bat`
- **Requirements:** Windows 10/11 (built-in PowerShell)
- **Just double-click** → Follow prompts → Done!

### Python Installer (Cross-Platform)
**File:** `install.py`
**✨ Recommended for all platforms**

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

### Bash Installer (Cross-Platform)
**File:** `install.sh`
**✨ Recommended for Git Bash/macOS/Linux users**

Works on:
- macOS
- Linux
- Windows (Git Bash, WSL)

**Basic usage:**
```bash
cd your-project
bash ../shipkit/installers/install.sh
```

**Advanced usage:**
```bash
# Install to specific directory
bash install.sh --target /path/to/project

# Non-interactive mode
bash install.sh /path/to/project -y

# Clone from GitHub and install
bash install.sh --github https://github.com/user/shipkit.git --target ~/my-project

# Show help
bash install.sh --help
```

## What Gets Installed

All installers create the same structure in your project:

```
your-project/
├── CLAUDE.md                 # Project instructions for Claude
├── .claude/
│   ├── settings.json         # Permissions + hooks
│   ├── skills/               # 24 skill definitions
│   ├── agents/               # 7 agent personas
│   └── hooks/                # Session enforcement
└── .shipkit/
    ├── scripts/bash/         # Shared utilities
    └── skills/               # 24 skill implementations
        */scripts/            # Automation
        */templates/          # Templates
        */references/         # Extended docs
        */outputs/            # Artifacts (protected)
```

## Future Installers

This directory is organized to support additional installation methods:

- **PowerShell installer** - Native Windows installation
- **NPM package** - `npm install -g shipkit`
- **Homebrew formula** - `brew install shipkit`
- **VS Code extension** - One-click install from marketplace
- **Docker image** - Pre-configured development environment

Each installer should:
1. Create the same file structure
2. Support the same core options (target directory, non-interactive mode)
3. Include comprehensive help documentation
4. Handle updates gracefully (preserve outputs, update definitions)
