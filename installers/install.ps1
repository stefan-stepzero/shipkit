# install.ps1 - Shipkit Installer (PowerShell)
# Requires PowerShell 5.1 or later

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetDir,

    [Parameter()]
    [string]$Target,

    [Parameter()]
    [string]$GitHubUrl,

    [Parameter()]
    [string]$Branch = "main",

    [Parameter()]
    [switch]$Yes,

    [Parameter()]
    [switch]$Help
)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$Interactive = -not $Yes
$TempDir = $null
$CleanupTemp = $false

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

function Write-Success { param([string]$Message) Write-Host "  ✓ $Message" -ForegroundColor Green }
function Write-Info { param([string]$Message) Write-Host "  → $Message" -ForegroundColor Cyan }
function Write-Warning { param([string]$Message) Write-Host "  ⚠ $Message" -ForegroundColor Yellow }
function Write-Error { param([string]$Message) Write-Host "  ✗ $Message" -ForegroundColor Red }
function Write-Bullet { param([string]$Message) Write-Host "  • $Message" -ForegroundColor DarkGray }

function Write-Loading {
    param([string]$Message)
    Write-Host "  → $Message" -NoNewline -ForegroundColor Cyan
    for ($i = 0; $i -lt 3; $i++) {
        Start-Sleep -Milliseconds 200
        Write-Host "." -NoNewline
    }
    Write-Host ""
}

function Clear-Screen {
    Clear-Host
}

function Show-Logo {
    Write-Host ""
    Write-Host "    ┌──────────────────────────────────────────────────────────────────────┐" -ForegroundColor Magenta
    Write-Host "    │                                                        /\            │" -ForegroundColor Magenta
    Write-Host "    │   ███████╗██╗  ██╗██╗██████╗ ██╗  ██╗██╗████████╗      /  \           │" -ForegroundColor Magenta
    Write-Host "    │   ██╔════╝██║  ██║██║██╔══██╗██║ ██╔╝██║╚══██╔══╝     / /| \          │" -ForegroundColor Magenta
    Write-Host "    │   ███████╗███████║██║██████╔╝█████╔╝ ██║   ██║       / / |  \         │" -ForegroundColor Magenta
    Write-Host "    │   ╚════██║██╔══██║██║██╔═══╝ ██╔═██╗ ██║   ██║      /_/__|___\        │" -ForegroundColor Magenta
    Write-Host "    │   ███████║██║  ██║██║██║     ██║  ██╗██║   ██║      \________/        │" -ForegroundColor Magenta
    Write-Host "    │   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝      ~~~~~~~~~~        │" -ForegroundColor Magenta
    Write-Host "    │                                                                      │" -ForegroundColor Magenta
    Write-Host "    └──────────────────────────────────────────────────────────────────────┘" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "         Complete Product Development Framework" -ForegroundColor DarkGray
    Write-Host "              24 Skills • 6 Agents • Constitution-Driven" -ForegroundColor DarkGray
    Write-Host ""
}

function Show-MiniLogo {
    Write-Host ""
    Write-Host "  ╭──────────────────────────────────────╮" -ForegroundColor Magenta
    Write-Host "  │  ShipKit • 24 Skills                 │" -ForegroundColor Magenta
    Write-Host "  ╰──────────────────────────────────────╯" -ForegroundColor Magenta
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

function Test-SourceFiles {
    Write-Host "  Verifying source files..." -ForegroundColor White
    Write-Host ""

    $RequiredPaths = @(
        "install\skills",
        "install\agents",
        "install\workspace\skills",
        "install\workspace\scripts",
        "install\hooks",
        "install\settings.json",
        "install\CLAUDE.md",
        "help"
    )

    $Missing = 0
    foreach ($Path in $RequiredPaths) {
        $FullPath = Join-Path $RepoRoot $Path
        if (Test-Path $FullPath) {
            Write-Success $Path
        } else {
            Write-Error "$Path (missing)"
            $Missing++
        }
    }

    Write-Host ""

    if ($Missing -gt 0) {
        Write-Error "Source directory is incomplete!"
        Write-Host ""
        Write-Host "  Expected shipkit structure at: $RepoRoot" -ForegroundColor DarkGray
        Write-Host ""
        return $false
    }

    return $true
}

function Test-ProjectRoot {
    return Test-Path ".git"
}

function Confirm-Action {
    param(
        [string]$Prompt,
        [string]$Default = "Y"
    )

    if (-not $Interactive) {
        return $true
    }

    $Hint = if ($Default -eq "Y") { "Y/n" } else { "y/N" }

    Write-Host "  $Prompt " -NoNewline -ForegroundColor White
    Write-Host "[$Hint] " -NoNewline -ForegroundColor DarkGray

    $Response = Read-Host

    if ([string]::IsNullOrWhiteSpace($Response)) {
        $Response = $Default
    }

    return $Response -match "^[Yy]"
}

function Get-TargetDirectory {
    Write-Host ""
    Write-Host "  Where would you like to install Shipkit?" -ForegroundColor White
    Write-Host "  (Press Enter for current directory: $PWD)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Install path: " -NoNewline -ForegroundColor Cyan

    $UserInput = Read-Host

    if ([string]::IsNullOrWhiteSpace($UserInput)) {
        return $PWD.Path
    } else {
        # Convert to absolute path if relative
        if (-not [System.IO.Path]::IsPathRooted($UserInput)) {
            return Join-Path $PWD $UserInput
        }
        return $UserInput
    }
}

function Open-HtmlDocs {
    $HtmlDir = Join-Path $RepoRoot "help"

    Write-Host ""
    Write-Host "  📖 Opening documentation..." -ForegroundColor Cyan
    Write-Host ""

    if (-not (Test-Path $HtmlDir)) {
        Write-Warning "Documentation files not found in $HtmlDir"
        return
    }

    $SkillsSummary = Join-Path $HtmlDir "skills-summary.html"
    $SystemOverview = Join-Path $HtmlDir "system-overview.html"

    if (Test-Path $SystemOverview) {
        try {
            Start-Process $SystemOverview
            Write-Success "Opened system-overview.html"
        } catch {
            Write-Warning "Could not open system-overview.html"
        }
    }

    if (Test-Path $SkillsSummary) {
        try {
            Start-Process $SkillsSummary
            Write-Success "Opened skills-summary.html"
        } catch {
            Write-Warning "Could not open skills-summary.html"
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

function Install-Skills {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  Installing skills" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""

    $SkillsDir = ".claude\skills"
    if (-not (Test-Path $SkillsDir)) {
        New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
    }

    Write-Loading "Installing skill definitions"

    $SourceSkills = Join-Path $RepoRoot "install\skills\*"
    Copy-Item -Path $SourceSkills -Destination $SkillsDir -Recurse -Force

    $SkillCount = (Get-ChildItem $SkillsDir -Directory).Count
    Write-Success "Installed $SkillCount skill definitions"
    Write-Bullet "12 product skills (prod-*)"
    Write-Bullet "9 development skills (dev-*)"
    Write-Bullet "3 meta skills (shipkit-master, dev-discussion, dev-writing-skills)"
}

function Install-Agents {
    Write-Host ""
    Write-Host "  Installing agent personas" -ForegroundColor White
    Write-Host ""

    $AgentsDir = ".claude\agents"
    if (-not (Test-Path $AgentsDir)) {
        New-Item -ItemType Directory -Path $AgentsDir -Force | Out-Null
    }

    $Count = 0
    $SourceAgents = Join-Path $RepoRoot "install\agents\*.md"
    Get-Item $SourceAgents -ErrorAction SilentlyContinue | ForEach-Object {
        # Skip README.md - it's documentation, not an agent definition
        if ($_.Name -eq "README.md") {
            Write-Info "  Skipping README.md (documentation only)"
            return
        }
        $DestFile = Join-Path $AgentsDir $_.Name
        if (-not (Test-Path $DestFile)) {
            Copy-Item $_.FullName -Destination $DestFile
            $Count++
        }
    }

    Write-Success "Installed $Count agent personas"
    Write-Bullet "prod-product-manager, prod-product-designer"
    Write-Bullet "dev-architect, dev-implementer, dev-reviewer"
    Write-Bullet "any-researcher"
}

function Install-Hooks {
    Write-Host ""
    Write-Host "  Installing session hooks" -ForegroundColor White
    Write-Host ""

    $HooksDir = ".claude\hooks"
    if (-not (Test-Path $HooksDir)) {
        New-Item -ItemType Directory -Path $HooksDir -Force | Out-Null
    }

    $SourceHooks = Join-Path $RepoRoot "install\hooks\*"
    Copy-Item -Path $SourceHooks -Destination $HooksDir -Recurse -Force

    Write-Success "Installed session hooks"
    Write-Bullet "SessionStart hook loads shipkit-master"
}

function Install-Settings {
    Write-Host ""
    Write-Host "  Installing settings.json" -ForegroundColor White
    Write-Host ""

    $SettingsFile = ".claude\settings.json"

    if (-not (Test-Path $SettingsFile)) {
        $SourceSettings = Join-Path $RepoRoot "install\settings.json"
        if (Test-Path $SourceSettings) {
            Copy-Item $SourceSettings -Destination $SettingsFile
            Write-Success "Installed settings.json"
            Write-Bullet "File protections: .claude/* and .shipkit/skills/*/outputs|templates|scripts"
            Write-Bullet "SessionStart hook configured"
            Write-Bullet "SkillComplete prompts enabled"
        } else {
            Write-Error "Source settings.json not found!"
            return $false
        }
    } else {
        Write-Warning "settings.json exists, preserving your custom config"
        Write-Info "Backup your settings before re-installing if needed"
    }

    return $true
}

function Install-Workspace {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  Setting up workspace" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""

    Write-Loading "Creating .shipkit/ workspace structure"

    # Create base directories
    if (-not (Test-Path ".shipkit\scripts")) {
        New-Item -ItemType Directory -Path ".shipkit\scripts" -Force | Out-Null
    }
    if (-not (Test-Path ".shipkit\skills")) {
        New-Item -ItemType Directory -Path ".shipkit\skills" -Force | Out-Null
    }

    # Copy shared scripts
    $SourceScripts = Join-Path $RepoRoot "install\workspace\scripts\bash"
    if (Test-Path $SourceScripts) {
        Copy-Item -Path $SourceScripts -Destination ".shipkit\scripts\" -Recurse -Force
        Write-Success "Installed shared scripts (common.sh)"
    }

    # Copy all skill implementations
    Write-Loading "Installing skill implementations (scripts, templates, references)"

    $SkillImplCount = 0
    $SourceSkills = Join-Path $RepoRoot "install\workspace\skills"
    if (Test-Path $SourceSkills) {
        Get-ChildItem $SourceSkills -Directory | ForEach-Object {
            $SkillName = $_.Name
            $DestSkillDir = ".shipkit\skills\$SkillName"

            if (-not (Test-Path $DestSkillDir)) {
                New-Item -ItemType Directory -Path $DestSkillDir -Force | Out-Null
            }

            # Copy scripts, templates, references
            @("scripts", "templates", "references") | ForEach-Object {
                $SourceSubDir = Join-Path $_.FullName $_
                if (Test-Path $SourceSubDir) {
                    Copy-Item -Path $SourceSubDir -Destination $DestSkillDir -Recurse -Force
                }
            }

            # Create empty outputs folder
            $OutputsDir = Join-Path $DestSkillDir "outputs"
            if (-not (Test-Path $OutputsDir)) {
                New-Item -ItemType Directory -Path $OutputsDir -Force | Out-Null
            }

            $SkillImplCount++
        }
    }

    Write-Success "Installed $SkillImplCount skill implementations"
    Write-Bullet "Scripts: Automation for each skill"
    Write-Bullet "Templates: Single adaptive template per skill"
    Write-Bullet "References: Extended docs, examples, patterns"
    Write-Bullet "Outputs: Empty (populated when skills run)"

    Write-Host ""
    Write-Success "Shipkit workspace ready"
    Write-Bullet "Unified .shipkit/ structure for all skills"
}

function Install-ClaudeMd {
    Write-Host ""
    Write-Host "  Installing CLAUDE.md" -ForegroundColor White
    Write-Host ""

    if (-not (Test-Path "CLAUDE.md")) {
        $SourceClaudeMd = Join-Path $RepoRoot "install\CLAUDE.md"
        if (Test-Path $SourceClaudeMd) {
            Copy-Item $SourceClaudeMd -Destination ".\CLAUDE.md"
            Write-Success "Installed CLAUDE.md (project instructions)"
            Write-Bullet "24 skill routing guide"
            Write-Bullet "Constitution-driven workflows"
            Write-Bullet "Product → Development integration"
        } else {
            Write-Error "Source CLAUDE.md not found!"
            return $false
        }
    } else {
        Write-Warning "CLAUDE.md exists, skipping"
        Write-Info "Delete existing CLAUDE.md if you want to reinstall"
    }

    return $true
}

function Normalize-LineEndings {
    Write-Host ""
    Write-Host "  Normalizing line endings" -ForegroundColor White
    Write-Host ""

    Write-Info "Converting hook scripts to Unix (LF) line endings..."

    $HooksDir = ".claude\hooks"
    $Count = 0

    Get-ChildItem "$HooksDir\*.sh" -ErrorAction SilentlyContinue | ForEach-Object {
        $content = [System.IO.File]::ReadAllText($_.FullName)
        $normalized = $content -replace "`r`n", "`n" -replace "`r", "`n"
        [System.IO.File]::WriteAllText($_.FullName, $normalized)
        $Count++
    }

    Write-Success "Normalized $Count hook scripts"
    Write-Bullet "All hooks now have Unix (LF) line endings"
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

function Show-Completion {
    param([string]$TargetPath)

    $SkillCount = (Get-ChildItem ".claude\skills" -Directory -ErrorAction SilentlyContinue).Count
    $AgentCount = (Get-ChildItem ".claude\agents\*.md" -ErrorAction SilentlyContinue).Count
    $SkillImplCount = (Get-ChildItem ".shipkit\skills" -Directory -ErrorAction SilentlyContinue).Count

    Write-Host ""
    Write-Host ""
    Write-Host "    ╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "    ║                                                           ║" -ForegroundColor Green
    Write-Host "    ║   ✓  Installation Complete!                               ║" -ForegroundColor Green
    Write-Host "    ║                                                           ║" -ForegroundColor Green
    Write-Host "    ╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""

    Write-Host "  What was installed:" -ForegroundColor White
    Write-Host ""
    Write-Success "$SkillCount skill definitions (.claude/skills/)"
    Write-Success "$SkillImplCount skill implementations (.shipkit/skills/)"
    Write-Success "$AgentCount agent personas (.claude/agents/)"
    Write-Success "Shared scripts (.shipkit/scripts/bash/common.sh)"
    Write-Success "Session hooks (.claude/hooks/)"
    Write-Success "Settings with file protections (.claude/settings.json)"
    Write-Success "Project instructions (CLAUDE.md)"

    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  Next Steps" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""

    Write-Host "  1. " -NoNewline -ForegroundColor Cyan
    Write-Host "Start Claude Code in " -NoNewline
    Write-Host "$TargetPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  2. " -NoNewline -ForegroundColor Cyan
    Write-Host "Choose your workflow:"
    Write-Host ""
    Write-Host "     Full product development (Greenfield):" -ForegroundColor DarkGray
    Write-Host "     /prod-strategic-thinking" -NoNewline -ForegroundColor Green
    Write-Host " → " -NoNewline
    Write-Host "/prod-constitution-builder" -ForegroundColor Green
    Write-Host "     → " -NoNewline
    Write-Host "/prod-personas" -NoNewline -ForegroundColor Green
    Write-Host " → " -NoNewline
    Write-Host "/prod-user-stories" -NoNewline -ForegroundColor Green
    Write-Host " → " -NoNewline
    Write-Host "/dev-specify" -ForegroundColor Green
    Write-Host ""
    Write-Host "     Quick POC (Fast validation):" -ForegroundColor DarkGray
    Write-Host "     /prod-constitution-builder" -NoNewline -ForegroundColor Green
    Write-Host " (choose POC)" -NoNewline -ForegroundColor DarkGray
    Write-Host " → " -NoNewline
    Write-Host "/dev-specify" -NoNewline -ForegroundColor Green
    Write-Host " → " -NoNewline
    Write-Host "/dev-implement" -ForegroundColor Green
    Write-Host ""
    Write-Host "     Existing codebase (Add feature):" -ForegroundColor DarkGray
    Write-Host "     /dev-constitution" -NoNewline -ForegroundColor Green
    Write-Host " → " -NoNewline
    Write-Host "/dev-specify" -NoNewline -ForegroundColor Green
    Write-Host " → " -NoNewline
    Write-Host "/dev-implement" -ForegroundColor Green
    Write-Host ""
    Write-Host "  3. " -NoNewline -ForegroundColor Cyan
    Write-Host "Type " -NoNewline
    Write-Host "/help" -NoNewline -ForegroundColor Green
    Write-Host " to see all 24 skills"
    Write-Host ""
    Write-Host "  💡 Constitution-Driven Development:" -ForegroundColor Cyan
    Write-Host "     Run " -NoNewline
    Write-Host "/prod-constitution-builder" -NoNewline -ForegroundColor Green
    Write-Host " to choose project type:"
    Write-Host "     • B2B/B2C Greenfield (comprehensive)" -ForegroundColor DarkGray
    Write-Host "     • Side Project MVP/POC (minimal)" -ForegroundColor DarkGray
    Write-Host "     • Experimental (learning-focused)" -ForegroundColor DarkGray
    Write-Host "     • Existing Project (document current state)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Happy shipping! 🚀" -ForegroundColor DarkGray
    Write-Host ""

    # Open documentation
    Open-HtmlDocs
}

# ═══════════════════════════════════════════════════════════════════════════════
# USAGE & CLI
# ═══════════════════════════════════════════════════════════════════════════════

function Show-Usage {
    @"
Usage: .\install.ps1 [TargetDir] [OPTIONS]

Install Shipkit framework into a target directory.

ARGUMENTS:
    TargetDir                  Target directory (optional, defaults to current directory)

OPTIONS:
    -Target <path>             Target directory (alternative to positional argument)
    -GitHubUrl <URL>           Clone from GitHub instead of local
    -Branch <name>             GitHub branch (default: main)
    -Yes                       Skip confirmations
    -Help                      Show this help

EXAMPLES:
    # Interactive mode in current directory
    .\install.ps1

    # Install to specific directory (positional)
    .\install.ps1 C:\Projects\MyProject

    # Install to specific directory (flag)
    .\install.ps1 -Target C:\Projects\MyProject

    # Non-interactive installation
    .\install.ps1 C:\Projects\MyProject -Yes

    # From GitHub to specific directory
    .\install.ps1 -Target C:\Projects\MyProject -GitHubUrl https://github.com/user/shipkit.git

WHAT GETS INSTALLED:
    .claude\
      skills\           24 skill definitions (SKILL.md files)
      agents\           6 agent personas
      hooks\            Session start hooks
      settings.json     Permissions and file protections

    .shipkit\
      skills\           24 skill implementations
        *\scripts\      Automation for each skill
        *\templates\    Templates (including 6 constitution templates)
        *\references\   Extended docs and examples
        *\outputs\      Empty (populated when skills run)
      scripts\
        bash\common.sh  Shared utilities

    CLAUDE.md           Project instructions for Claude

CONSTITUTION SELECTION:
    Constitution templates are NOT selected during install.
    Run /prod-constitution-builder to choose from 6 project types:
      • B2B SaaS Greenfield
      • B2C SaaS Greenfield
      • Experimental
      • Side Project MVP
      • Side Project POC
      • Existing Project

"@
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

function Main {
    # Show help if requested
    if ($Help) {
        Show-Usage
        return
    }

    # Determine target directory
    if ($Target) {
        $Script:TargetDir = $Target
    } elseif (-not $TargetDir -and $Interactive -and -not $GitHubUrl) {
        $Script:TargetDir = Get-TargetDirectory
    } elseif (-not $TargetDir) {
        $Script:TargetDir = $PWD.Path
    }

    # Convert to absolute path
    if (-not [System.IO.Path]::IsPathRooted($TargetDir)) {
        $Script:TargetDir = Join-Path $PWD $TargetDir
    }

    # Create target directory if it doesn't exist
    if (-not (Test-Path $TargetDir)) {
        if ($Interactive) {
            Write-Host ""
            if (-not (Confirm-Action "Target directory $TargetDir doesn't exist. Create it?")) {
                Write-Info "Installation cancelled."
                return
            }
        }
        New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    }

    # Change to target directory
    Push-Location $TargetDir

    try {
        # Handle GitHub mode
        if ($GitHubUrl) {
            Show-MiniLogo
            Write-Info "Cloning from GitHub..."
            Write-Bullet "URL: $GitHubUrl"
            Write-Bullet "Branch: $Branch"
            Write-Host ""

            if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
                Write-Error "git is not installed"
                return
            }

            $Script:TempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
            $Script:CleanupTemp = $true

            $GitOutput = git clone --depth 1 --branch $Branch $GitHubUrl $TempDir.FullName 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Repository cloned"
                $Script:RepoRoot = $TempDir.FullName
            } else {
                Write-Error "Failed to clone repository"
                Write-Host ""
                Write-Warning "Common causes:"
                Write-Bullet "Repository is private (requires authentication)"
                Write-Bullet "Invalid URL or branch name"
                Write-Bullet "Network connectivity issues"
                Write-Host ""
                Write-Info "For private repos, clone manually first:"
                Write-Host "  git clone $GitHubUrl C:\your\path" -ForegroundColor DarkGray
                Write-Host "  cd C:\your\path" -ForegroundColor DarkGray
                Write-Host "  .\install.ps1" -ForegroundColor DarkGray
                Write-Host ""
                return
            }
            Write-Host ""
        }

        # Show logo
        if ($Interactive) {
            Clear-Screen
        }
        Show-Logo

        # Detect and verify
        Write-Host "  Detecting installation context..." -ForegroundColor White
        Write-Host ""
        Write-Info "Source: $RepoRoot"
        Write-Info "Target: $TargetDir"
        Write-Host ""

        if (-not (Test-SourceFiles)) {
            return
        }

        # Check project root
        if (-not (Test-ProjectRoot)) {
            Write-Host ""
            Write-Warning "No .git directory found. This might not be a project root."
            if ($Interactive) {
                if (-not (Confirm-Action "Continue anyway?")) {
                    Write-Info "Installation cancelled."
                    return
                }
            }
        }

        # Confirm installation location
        if ($Interactive) {
            Write-Host ""
            if (-not (Confirm-Action "Install Shipkit to $TargetDir?")) {
                Write-Info "Installation cancelled."
                return
            }
        }

        # Perform installation
        Write-Host ""
        Write-Info "Installing Shipkit framework..."

        Install-Skills
        Install-Agents
        Install-Hooks
        Install-Settings
        Install-Workspace
        Install-ClaudeMd
        Normalize-LineEndings

        # Show completion
        Show-Completion -TargetPath $TargetDir

    } finally {
        Pop-Location

        # Cleanup temp directory if needed
        if ($CleanupTemp -and $TempDir -and (Test-Path $TempDir)) {
            Remove-Item $TempDir -Recurse -Force
        }
    }
}

# Run main
Main
