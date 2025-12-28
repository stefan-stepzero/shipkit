# install.ps1 - Shipkit Installer (PowerShell - Manifest-Based)
# Requires PowerShell 5.1 or later

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet('lite', 'default')]
    [string]$Profile,

    [Parameter()]
    [ValidateSet('bash', 'python')]
    [string]$Language,

    [Parameter()]
    [string]$Target,

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
$TargetDir = ""
$Interactive = -not $Yes

# Manifest data (populated after loading)
$Script:ManifestEdition = ""
$Script:ManifestDescription = ""
$Script:ManifestSettingsFile = ""
$Script:ManifestClaudeMdFile = ""
$Script:ManifestSkillsDefinitions = @()
$Script:ManifestSkillsWorkspace = @()
$Script:ManifestAgents = @()

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

# ═══════════════════════════════════════════════════════════════════════════════
# MANIFEST LOADING
# ═══════════════════════════════════════════════════════════════════════════════

function Load-Manifest {
    param([string]$ProfileName)

    $ManifestFile = Join-Path $RepoRoot "install\profiles\$ProfileName.manifest.json"

    if (-not (Test-Path $ManifestFile)) {
        Write-Error "Manifest not found: $ManifestFile"
        exit 1
    }

    Write-Info "Loading manifest: $ProfileName.manifest.json"

    try {
        $Manifest = Get-Content $ManifestFile -Raw | ConvertFrom-Json

        $Script:ManifestEdition = $Manifest.edition
        $Script:ManifestDescription = $Manifest.description
        $Script:ManifestSettingsFile = $Manifest.settingsFile
        $Script:ManifestClaudeMdFile = $Manifest.claudeMdFile
        $Script:ManifestSkillsDefinitions = $Manifest.skills.definitions
        $Script:ManifestSkillsWorkspace = $Manifest.skills.workspace
        $Script:ManifestAgents = $Manifest.agents

        Write-Success "Loaded $($Script:ManifestEdition) edition manifest"
    }
    catch {
        Write-Error "Failed to parse manifest: $_"
        exit 1
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

function Get-ProfileSelection {
    Write-Host ""
    Write-Host "  Select Edition" -ForegroundColor White
    Write-Host ""
    Write-Host "  [1] " -NoNewline -ForegroundColor Cyan
    Write-Host "Lite      " -NoNewline -ForegroundColor White
    Write-Host "- Fast, minimal (7 skills, POCs and side projects)"
    Write-Host "  [2] " -NoNewline -ForegroundColor Cyan
    Write-Host "Default   " -NoNewline -ForegroundColor White
    Write-Host "- Complete (24 skills, full product development)"
    Write-Host ""
    Write-Host "  Select edition [1-2]: " -NoNewline -ForegroundColor Cyan

    $Choice = Read-Host

    switch ($Choice) {
        "1" {
            Write-Host ""
            Write-Success "Selected: Lite Edition"
            return "lite"
        }
        "2" {
            Write-Host ""
            Write-Success "Selected: Default Edition"
            return "default"
        }
        default {
            Write-Host ""
            Write-Warning "Invalid choice. Defaulting to Default Edition."
            return "default"
        }
    }
}

function Get-LanguageSelection {
    Write-Host ""
    Write-Host "  Select Scripting Language" -ForegroundColor White
    Write-Host ""
    Write-Host "  [1] " -NoNewline -ForegroundColor Cyan
    Write-Host "Bash      " -NoNewline -ForegroundColor White
    Write-Host "- Traditional shell scripts (cross-platform)"
    Write-Host "  [2] " -NoNewline -ForegroundColor Cyan
    Write-Host "Python    " -NoNewline -ForegroundColor White
    Write-Host "- Python scripts (recommended for Windows)"
    Write-Host ""
    Write-Host "  Select language [1-2]: " -NoNewline -ForegroundColor Cyan

    $Choice = Read-Host

    switch ($Choice) {
        "1" {
            Write-Host ""
            Write-Success "Selected: Bash"
            return "bash"
        }
        "2" {
            Write-Host ""
            Write-Success "Selected: Python"
            return "python"
        }
        default {
            Write-Host ""
            Write-Warning "Invalid choice. Defaulting to Python."
            return "python"
        }
    }
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
        if (-not [System.IO.Path]::IsPathRooted($UserInput)) {
            return Join-Path $PWD $UserInput
        }
        return $UserInput
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# ASCII ART HEADER
# ═══════════════════════════════════════════════════════════════════════════════

function Show-Logo {
    param([string]$Edition = "default")

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

    if ($Edition -eq "lite") {
        Write-Host "         Lightweight Product Development Framework" -ForegroundColor DarkGray
        Write-Host "              7 Skills • Streamlined Workflows" -ForegroundColor DarkGray
    } else {
        Write-Host "         Complete Product Development Framework" -ForegroundColor DarkGray
        Write-Host "              24 Skills • 6 Agents • Constitution-Driven" -ForegroundColor DarkGray
    }
    Write-Host ""
}

function Show-MiniLogo {
    Write-Host ""
    Write-Host "  ╭──────────────────────────────────────╮" -ForegroundColor Magenta
    Write-Host "  │  ShipKit • Manifest-Based Install   │" -ForegroundColor Magenta
    Write-Host "  ╰──────────────────────────────────────╯" -ForegroundColor Magenta
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

function Show-InstallationContext {
    param([string]$ProfileName, [string]$LanguageName)

    Write-Host "  Installation Context" -ForegroundColor White
    Write-Host ""
    Write-Info "Source: $RepoRoot"
    Write-Info "Target: $TargetDir"
    Write-Info "Edition: $ProfileName"
    Write-Info "Language: $LanguageName"
    Write-Host ""
}

function Test-SourceFiles {
    Write-Host "  Verifying source files..." -ForegroundColor White
    Write-Host ""

    $RequiredPaths = @(
        "install\shared",
        "install\skills",
        "install\agents",
        "install\workspace\skills",
        "install\settings",
        "install\claude-md",
        "install\profiles",
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

function Open-HtmlDocs {
    $HtmlDir = Join-Path $RepoRoot "help"

    Write-Host ""
    Write-Host "  📖 Opening documentation..." -ForegroundColor Cyan
    Write-Host ""

    if (-not (Test-Path $HtmlDir)) {
        Write-Warning "Documentation files not found in $HtmlDir"
        return
    }

    # Choose appropriate overview based on edition
    if ($Script:Profile -eq "lite") {
        $OverviewFile = Join-Path $HtmlDir "shipkit-lite-overview.html"
    } else {
        $OverviewFile = Join-Path $HtmlDir "system-overview.html"
    }

    if (-not (Test-Path $OverviewFile)) {
        Write-Warning "Overview not found: $OverviewFile"
        return
    }

    try {
        Start-Process $OverviewFile
        $OverviewName = Split-Path $OverviewFile -Leaf
        Write-Success "Opened $OverviewName"
    } catch {
        $OverviewName = Split-Path $OverviewFile -Leaf
        Write-Warning "Could not open $OverviewName"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

function Install-SharedCore {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  Installing shared core files" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""

    # Install hooks (edition-specific)
    Write-Info "Installing session hooks..."
    $HooksDir = ".claude\hooks"
    if (-not (Test-Path $HooksDir)) {
        New-Item -ItemType Directory -Path $HooksDir -Force | Out-Null
    }

    $HooksSource = Join-Path $RepoRoot "install\shared\hooks"
    if ($Script:Profile -eq "lite") {
        # Install lite-specific hooks
        Copy-Item -Path (Join-Path $HooksSource "lite-session-start.py") -Destination (Join-Path $HooksDir "session-start.py") -Force
        Copy-Item -Path (Join-Path $HooksSource "lite-suggest-next-skill.py") -Destination (Join-Path $HooksDir "suggest-next-skill.py") -Force
        Write-Success "Installed session hooks (lite edition)"
    } else {
        # Install full Shipkit hooks
        Copy-Item -Path (Join-Path $HooksSource "session-start.py") -Destination (Join-Path $HooksDir "session-start.py") -Force
        Copy-Item -Path (Join-Path $HooksSource "suggest-next-skill.py") -Destination (Join-Path $HooksDir "suggest-next-skill.py") -Force
        Write-Success "Installed session hooks (full edition)"
    }

    # Install scripts
    Write-Info "Installing shared scripts..."
    if (-not (Test-Path ".shipkit\scripts\bash")) {
        New-Item -ItemType Directory -Path ".shipkit\scripts\bash" -Force | Out-Null
    }
    if (-not (Test-Path ".shipkit\scripts\python")) {
        New-Item -ItemType Directory -Path ".shipkit\scripts\python" -Force | Out-Null
    }

    $SourceBashScripts = Join-Path $RepoRoot "install\shared\scripts\bash\*"
    $SourcePythonScripts = Join-Path $RepoRoot "install\shared\scripts\python\*"

    Copy-Item -Path $SourceBashScripts -Destination ".shipkit\scripts\bash\" -Force -ErrorAction SilentlyContinue
    Copy-Item -Path $SourcePythonScripts -Destination ".shipkit\scripts\python\" -Force -ErrorAction SilentlyContinue
    Write-Success "Installed shared scripts"

    # Install git files
    Write-Info "Installing git configuration files..."

    $SourceGitIgnore = Join-Path $RepoRoot "install\shared\.gitignore"
    if (-not (Test-Path ".gitignore") -and (Test-Path $SourceGitIgnore)) {
        Copy-Item $SourceGitIgnore -Destination ".\.gitignore"
        Write-Success "Installed .gitignore"
    } else {
        Write-Warning ".gitignore exists, skipping"
    }

    # No longer install .gitattributes - hooks are Python now (no line ending issues)
}

function Install-EditionFiles {
    param([string]$ProfileName)

    Write-Host ""
    Write-Host "  Installing edition-specific files" -ForegroundColor White
    Write-Host ""

    # Install settings.json
    Write-Info "Installing settings.json for $ProfileName edition..."
    if (-not (Test-Path ".claude")) {
        New-Item -ItemType Directory -Path ".claude" -Force | Out-Null
    }

    $SettingsSource = Join-Path $RepoRoot "install\settings\$($Script:ManifestSettingsFile)"

    if (-not (Test-Path ".claude\settings.json")) {
        Copy-Item $SettingsSource -Destination ".claude\settings.json"
        Write-Success "Installed settings.json"
    } else {
        Write-Warning "settings.json exists, preserving your custom config"
    }

    # Install CLAUDE.md
    Write-Info "Installing CLAUDE.md for $ProfileName edition..."
    $ClaudeMdSource = Join-Path $RepoRoot "install\claude-md\$($Script:ManifestClaudeMdFile)"

    if (-not (Test-Path "CLAUDE.md")) {
        Copy-Item $ClaudeMdSource -Destination ".\CLAUDE.md"
        Write-Success "Installed CLAUDE.md"
    } else {
        Write-Warning "CLAUDE.md exists, skipping"
    }
}

function Install-Skills {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  Installing skills" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""

    if (-not (Test-Path ".claude\skills")) {
        New-Item -ItemType Directory -Path ".claude\skills" -Force | Out-Null
    }
    if (-not (Test-Path ".shipkit\skills")) {
        New-Item -ItemType Directory -Path ".shipkit\skills" -Force | Out-Null
    }

    # Install skill definitions
    Write-Info "Installing skill definitions..."
    $DefCount = 0
    foreach ($Skill in $Script:ManifestSkillsDefinitions) {
        if ([string]::IsNullOrWhiteSpace($Skill)) { continue }
        $SourceSkill = Join-Path $RepoRoot "install\skills\$Skill"
        if (Test-Path $SourceSkill) {
            Copy-Item -Path $SourceSkill -Destination ".claude\skills\" -Recurse -Force
            $DefCount++
        }
    }
    Write-Success "Installed $DefCount skill definitions"

    # Install skill implementations (workspace)
    Write-Info "Installing skill implementations..."
    $ImplCount = 0
    foreach ($Skill in $Script:ManifestSkillsWorkspace) {
        if ([string]::IsNullOrWhiteSpace($Skill)) { continue }
        $SourceSkill = Join-Path $RepoRoot "install\workspace\skills\$Skill"
        if (Test-Path $SourceSkill) {
            $DestSkillDir = ".shipkit\skills\$Skill"
            if (-not (Test-Path $DestSkillDir)) {
                New-Item -ItemType Directory -Path $DestSkillDir -Force | Out-Null
            }

            # Copy scripts, templates, references
            @("scripts", "templates", "references") | ForEach-Object {
                $SourceSubDir = Join-Path $SourceSkill $_
                if (Test-Path $SourceSubDir) {
                    Copy-Item -Path $SourceSubDir -Destination $DestSkillDir -Recurse -Force
                }
            }

            # Create empty outputs folder
            $OutputsDir = Join-Path $DestSkillDir "outputs"
            if (-not (Test-Path $OutputsDir)) {
                New-Item -ItemType Directory -Path $OutputsDir -Force | Out-Null
            }

            $ImplCount++
        }
    }
    Write-Success "Installed $ImplCount skill implementations"
}

function Install-Agents {
    Write-Host ""
    Write-Host "  Installing agent personas" -ForegroundColor White
    Write-Host ""

    if ($Script:ManifestAgents.Count -eq 0) {
        Write-Info "No agents in manifest, skipping"
        return
    }

    if (-not (Test-Path ".claude\agents")) {
        New-Item -ItemType Directory -Path ".claude\agents" -Force | Out-Null
    }

    $Count = 0
    foreach ($Agent in $Script:ManifestAgents) {
        if ([string]::IsNullOrWhiteSpace($Agent)) { continue }
        $SourceAgent = Join-Path $RepoRoot "install\agents\$Agent.md"
        if (Test-Path $SourceAgent) {
            Copy-Item $SourceAgent -Destination ".claude\agents\"
            $Count++
        }
    }

    Write-Success "Installed $Count agent personas"
}

function Remove-UnusedLanguage {
    param([string]$SelectedLanguage)

    Write-Host ""
    Write-Host "  Removing unused language scripts" -ForegroundColor White
    Write-Host ""

    if ($SelectedLanguage -eq "bash") {
        Write-Info "Removing Python scripts (.py files)..."
        Get-ChildItem ".shipkit\skills" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue | Remove-Item -Force
        Get-ChildItem ".shipkit\scripts\python" -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force
        Write-Success "Removed Python scripts"
    }
    elseif ($SelectedLanguage -eq "python") {
        Write-Info "Removing Bash scripts (.sh files)..."
        Get-ChildItem ".shipkit\skills" -Recurse -Filter "*.sh" -ErrorAction SilentlyContinue | Remove-Item -Force
        Get-ChildItem ".shipkit\scripts\bash" -Recurse -Filter "*.sh" -ErrorAction SilentlyContinue | Remove-Item -Force
        Write-Success "Removed Bash scripts"
    }
}

function Normalize-LineEndings {
    Write-Host ""
    Write-Host "  Normalizing line endings" -ForegroundColor White
    Write-Host ""

    Write-Info "Converting hook scripts to Unix (LF) line endings..."

    $Count = 0
    Get-ChildItem ".claude\hooks\*.sh" -ErrorAction SilentlyContinue | ForEach-Object {
        $Content = [System.IO.File]::ReadAllText($_.FullName)
        $Normalized = $Content -replace "`r`n", "`n" -replace "`r", "`n"
        [System.IO.File]::WriteAllText($_.FullName, $Normalized)
        $Count++
    }

    if ($Count -gt 0) {
        Write-Success "Normalized $Count hook scripts"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

function Show-Completion {
    param(
        [string]$TargetPath,
        [string]$ProfileName,
        [string]$LanguageName
    )

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
    Write-Success "Edition: $ProfileName"
    Write-Success "Language: $LanguageName"
    Write-Success "$SkillCount skill definitions (.claude/skills/)"
    Write-Success "$SkillImplCount skill implementations (.shipkit/skills/)"

    if ($AgentCount -gt 0) {
        Write-Success "$AgentCount agent personas (.claude/agents/)"
    }

    Write-Success "Shared scripts (.shipkit/scripts/$LanguageName/)"
    Write-Success "Session hooks (.claude/hooks/)"
    Write-Success "Settings (.claude/settings.json)"
    Write-Success "Project instructions (CLAUDE.md)"
    Write-Success "Git configuration (.gitignore)"

    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  Next Steps" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""

    Write-Host "  1. " -NoNewline -ForegroundColor Cyan
    Write-Host "Start Claude Code in " -NoNewline
    Write-Host "$TargetPath" -ForegroundColor Cyan
    Write-Host ""

    if ($ProfileName -eq "lite") {
        Write-Host "  2. " -NoNewline -ForegroundColor Cyan
        Write-Host "Quick Start (Lite Edition):"
        Write-Host ""
        Write-Host "     /lite-project-context" -NoNewline -ForegroundColor Green
        Write-Host " → " -NoNewline
        Write-Host "/lite-spec" -ForegroundColor Green
        Write-Host "     → " -NoNewline
        Write-Host "/lite-plan" -NoNewline -ForegroundColor Green
        Write-Host " → " -NoNewline
        Write-Host "/lite-implement" -ForegroundColor Green
        Write-Host ""
    }
    else {
        Write-Host "  2. " -NoNewline -ForegroundColor Cyan
        Write-Host "Choose your workflow:"
        Write-Host ""
        Write-Host "     Full product development:" -ForegroundColor DarkGray
        Write-Host "     /prod-strategic-thinking" -NoNewline -ForegroundColor Green
        Write-Host " → " -NoNewline
        Write-Host "/prod-constitution-builder" -ForegroundColor Green
        Write-Host "     → " -NoNewline
        Write-Host "/prod-personas" -NoNewline -ForegroundColor Green
        Write-Host " → " -NoNewline
        Write-Host "/prod-user-stories" -ForegroundColor Green
        Write-Host ""
        Write-Host "     Quick POC:" -ForegroundColor DarkGray
        Write-Host "     /prod-constitution-builder" -NoNewline -ForegroundColor Green
        Write-Host " → " -NoNewline
        Write-Host "/dev-specify" -NoNewline -ForegroundColor Green
        Write-Host " → " -NoNewline
        Write-Host "/dev-implement" -ForegroundColor Green
        Write-Host ""
    }

    Write-Host "  3. " -NoNewline -ForegroundColor Cyan
    Write-Host "Type " -NoNewline
    if ($ProfileName -eq "lite") {
        Write-Host "/lite-project-status" -NoNewline -ForegroundColor Green
        Write-Host " to see current state"
    } else {
        Write-Host "/shipkit-status" -NoNewline -ForegroundColor Green
        Write-Host " to see current state"
    }
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
Usage: .\install.ps1 [OPTIONS]

Install Shipkit framework into a target directory.

OPTIONS:
    -Profile <lite|default>    Edition to install (default: prompts interactively)
    -Language <bash|python>    Scripting language (default: prompts interactively)
    -Target <path>             Target directory (default: prompts interactively)
    -Yes                       Skip confirmations
    -Help                      Show this help

EXAMPLES:
    # Interactive mode (prompts for all options)
    .\install.ps1

    # Install lite edition with Python to current directory
    .\install.ps1 -Profile lite -Language python -Yes

    # Install default edition with Bash to specific directory
    .\install.ps1 -Profile default -Language bash -Target C:\Projects\MyProject

    # Install to specific directory (interactive prompts for profile/language)
    .\install.ps1 -Target C:\Projects\MyProject

EDITIONS:
    lite      - Fast, minimal (7 skills, POCs and side projects)
    default   - Complete (24 skills, full product development)

LANGUAGES:
    bash      - Traditional shell scripts (cross-platform)
    python    - Python scripts (recommended for Windows)

WHAT GETS INSTALLED:
    .claude\
      skills\           Skill definitions (SKILL.md files)
      agents\           Agent personas (if any in manifest)
      hooks\            Session start hooks
      settings.json     Edition-specific settings

    .shipkit\
      skills\           Skill implementations
        *\scripts\      Automation (in selected language)
        *\templates\    Templates
        *\references\   Extended docs
        *\outputs\      Empty (populated when skills run)
      scripts\
        bash\ or python\  Shared utilities

    CLAUDE.md           Edition-specific project instructions
    .gitignore          Git ignore file

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

    # Prompt for profile if not specified
    if (-not $Profile) {
        if ($Interactive) {
            Clear-Screen
            Show-Logo
            $Script:Profile = Get-ProfileSelection
        } else {
            Write-Error "Profile not specified. Use -Profile lite or -Profile default"
            exit 1
        }
    }

    # Validate profile
    if ($Profile -ne "lite" -and $Profile -ne "default") {
        Write-Error "Invalid profile: $Profile. Must be 'lite' or 'default'"
        exit 1
    }

    # Prompt for language if not specified
    if (-not $Language) {
        if ($Interactive) {
            $Script:Language = Get-LanguageSelection
        } else {
            Write-Error "Language not specified. Use -Language bash or -Language python"
            exit 1
        }
    }

    # Validate language
    if ($Language -ne "bash" -and $Language -ne "python") {
        Write-Error "Invalid language: $Language. Must be 'bash' or 'python'"
        exit 1
    }

    # Load manifest
    Load-Manifest -ProfileName $Profile

    # Determine target directory
    if (-not $Target) {
        if ($Interactive) {
            $Script:TargetDir = Get-TargetDirectory
        } else {
            $Script:TargetDir = $PWD.Path
        }
    } else {
        $Script:TargetDir = $Target
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
        # Show logo if not already shown
        if ($Interactive -and $Language) {
            Clear-Screen
            Show-Logo -Edition $Profile
        }
        elseif (-not $Interactive) {
            Show-MiniLogo
        }

        # Show context and verify
        Show-InstallationContext -ProfileName $Profile -LanguageName $Language

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
            if (-not (Confirm-Action "Install Shipkit $Profile edition to $TargetDir?")) {
                Write-Info "Installation cancelled."
                return
            }
        }

        # Perform installation
        Write-Host ""
        Write-Info "Installing Shipkit framework..."

        Install-SharedCore
        Install-EditionFiles -ProfileName $Profile
        Install-Skills
        Install-Agents
        Remove-UnusedLanguage -SelectedLanguage $Language
        Normalize-LineEndings

        # Show completion
        Show-Completion -TargetPath $TargetDir -ProfileName $Profile -LanguageName $Language

    } finally {
        Pop-Location
    }
}

# Run main
Main
