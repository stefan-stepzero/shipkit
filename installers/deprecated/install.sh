#!/usr/bin/env bash
# install.sh - Shipkit Installer (Manifest-Based)
set -e

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS & STYLING
# ═══════════════════════════════════════════════════════════════════════════════

BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'
NC='\033[0m'

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'

# Bright colors
BRIGHT_GREEN='\033[1;32m'
BRIGHT_CYAN='\033[1;36m'
BRIGHT_MAGENTA='\033[1;35m'
BRIGHT_WHITE='\033[1;37m'

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
TARGET_DIR=""
PROFILE=""
LANGUAGE=""
INTERACTIVE=true
GITHUB_URL=""
GITHUB_BRANCH="main"
TEMP_DIR=""
CLEANUP_TEMP=false

# Manifest data (populated after loading)
MANIFEST_EDITION=""
MANIFEST_DESCRIPTION=""
MANIFEST_SETTINGS_FILE=""
MANIFEST_CLAUDE_MD_FILE=""
MANIFEST_SKILLS_DEFINITIONS=()
MANIFEST_SKILLS_WORKSPACE=()
MANIFEST_AGENTS=()

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

cleanup() {
    if [ "$CLEANUP_TEMP" = true ] && [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT

clear_screen() {
    printf "\033c"
}

print_success() { echo -e "  ${GREEN}✓${NC} $1"; }
print_info() { echo -e "  ${CYAN}→${NC} $1"; }
print_warning() { echo -e "  ${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "  ${RED}✗${NC} $1"; }
print_bullet() { echo -e "  ${DIM}•${NC} $1"; }

print_loading() {
    local msg="$1"
    echo -ne "  ${CYAN}→${NC} $msg"
    for i in {1..3}; do
        sleep 0.2
        echo -n "."
    done
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# MANIFEST LOADING
# ═══════════════════════════════════════════════════════════════════════════════

load_manifest() {
    local profile="$1"
    local manifest_file="$REPO_ROOT/install/profiles/${profile}.manifest.json"

    if [ ! -f "$manifest_file" ]; then
        print_error "Manifest not found: $manifest_file"
        exit 1
    fi

    print_info "Loading manifest: ${profile}.manifest.json"

    # Use Python to parse JSON (more reliable than jq dependency)
    local manifest_json
    manifest_json=$(python3 -c "
import json
import sys

try:
    with open('$manifest_file', 'r') as f:
        data = json.load(f)

    # Output key fields
    print('EDITION=' + data.get('edition', ''))
    print('DESCRIPTION=' + data.get('description', ''))
    print('SETTINGS_FILE=' + data.get('settingsFile', ''))
    print('CLAUDE_MD_FILE=' + data.get('claudeMdFile', ''))

    # Output skills (definitions)
    skills_defs = data.get('skills', {}).get('definitions', [])
    print('SKILLS_DEFINITIONS=' + ','.join(skills_defs))

    # Output skills (workspace)
    skills_workspace = data.get('skills', {}).get('workspace', [])
    print('SKILLS_WORKSPACE=' + ','.join(skills_workspace))

    # Output agents
    agents = data.get('agents', [])
    print('AGENTS=' + ','.join(agents))

except Exception as e:
    print(f'ERROR: Failed to parse manifest: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1)

    if [ $? -ne 0 ]; then
        print_error "Failed to parse manifest"
        echo "$manifest_json"
        exit 1
    fi

    # Parse output into variables
    while IFS='=' read -r key value; do
        case "$key" in
            EDITION) MANIFEST_EDITION="$value" ;;
            DESCRIPTION) MANIFEST_DESCRIPTION="$value" ;;
            SETTINGS_FILE) MANIFEST_SETTINGS_FILE="$value" ;;
            CLAUDE_MD_FILE) MANIFEST_CLAUDE_MD_FILE="$value" ;;
            SKILLS_DEFINITIONS) IFS=',' read -ra MANIFEST_SKILLS_DEFINITIONS <<< "$value" ;;
            SKILLS_WORKSPACE) IFS=',' read -ra MANIFEST_SKILLS_WORKSPACE <<< "$value" ;;
            AGENTS) IFS=',' read -ra MANIFEST_AGENTS <<< "$value" ;;
        esac
    done <<< "$manifest_json"

    print_success "Loaded ${MANIFEST_EDITION} edition manifest"
}

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

prompt_for_profile() {
    echo ""
    echo -e "  ${BOLD}Select Edition${NC}"
    echo ""
    echo -e "  ${CYAN}[1]${NC} ${BOLD}Lite${NC}      - Fast, minimal (7 skills, POCs and side projects)"
    echo -e "  ${CYAN}[2]${NC} ${BOLD}Default${NC}   - Complete (24 skills, full product development)"
    echo ""
    echo -ne "  ${CYAN}Select edition [1-2]:${NC} "
    read -r choice

    case "$choice" in
        1)
            PROFILE="lite"
            echo ""
            print_success "Selected: Lite Edition"
            ;;
        2)
            PROFILE="default"
            echo ""
            print_success "Selected: Default Edition"
            ;;
        *)
            echo ""
            print_warning "Invalid choice. Defaulting to Default Edition."
            PROFILE="default"
            ;;
    esac
}

prompt_for_language() {
    echo ""
    echo -e "  ${BOLD}Select Scripting Language${NC}"
    echo ""
    echo -e "  ${CYAN}[1]${NC} ${BOLD}Bash${NC}      - Traditional shell scripts (cross-platform)"
    echo -e "  ${CYAN}[2]${NC} ${BOLD}Python${NC}    - Python scripts (recommended for Windows)"
    echo ""
    echo -ne "  ${CYAN}Select language [1-2]:${NC} "
    read -r choice

    case "$choice" in
        1)
            LANGUAGE="bash"
            echo ""
            print_success "Selected: Bash"
            ;;
        2)
            LANGUAGE="python"
            echo ""
            print_success "Selected: Python"
            ;;
        *)
            echo ""
            print_warning "Invalid choice. Defaulting to Python."
            LANGUAGE="python"
            ;;
    esac
}

prompt_for_directory() {
    echo ""
    echo -e "  ${BOLD}Where would you like to install Shipkit?${NC}"
    echo -e "  ${DIM}(Press Enter for current directory: $PWD)${NC}"
    echo ""
    echo -ne "  ${CYAN}Install path:${NC} "
    read -r user_input

    if [ -z "$user_input" ]; then
        TARGET_DIR="$PWD"
    else
        TARGET_DIR="$user_input"
    fi

    # Convert to absolute path
    if [[ "$TARGET_DIR" != /* ]] && [[ ! "$TARGET_DIR" =~ ^[A-Za-z]:[/\\] ]]; then
        TARGET_DIR="$PWD/$TARGET_DIR"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# ASCII ART HEADER
# ═══════════════════════════════════════════════════════════════════════════════

show_logo() {
    local edition="${1:-default}"

    echo ""
    echo -e "${BRIGHT_MAGENTA}"
    cat << 'EOF'
    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                        /\            │
    │   ███████╗██╗  ██╗██╗██████╗ ██╗  ██╗██╗████████╗     /  \           │
    │   ██╔════╝██║  ██║██║██╔══██╗██║ ██╔╝██║╚══██╔══╝    / /| \          │
    │   ███████╗███████║██║██████╔╝█████╔╝ ██║   ██║      / / |  \         │
    │   ╚════██║██╔══██║██║██╔═══╝ ██╔═██╗ ██║   ██║     /_/__|___\        │
    │   ███████║██║  ██║██║██║     ██║  ██╗██║   ██║     \________/        │
    │   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝     ~~~~~~~~~~        │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘
EOF
    echo -e "${NC}"

    if [ "$edition" = "lite" ]; then
        echo -e "${DIM}         Lightweight Product Development Framework${NC}"
        echo -e "${DIM}              7 Skills • Streamlined Workflows${NC}"
    else
        echo -e "${DIM}         Complete Product Development Framework${NC}"
        echo -e "${DIM}              29 Skills • 7 Agents • Constitution-Driven${NC}"
    fi
    echo ""
}

show_mini_logo() {
    echo ""
    echo -e "${BRIGHT_MAGENTA}  ╭──────────────────────────────────────╮${NC}"
    echo -e "${BRIGHT_MAGENTA}  │${NC}  ${BOLD}ShipKit${NC} ${DIM}• Manifest-Based Install${NC}   ${BRIGHT_MAGENTA}│${NC}"
    echo -e "${BRIGHT_MAGENTA}  ╰──────────────────────────────────────╯${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

detect_installation_context() {
    echo -e "  ${BOLD}Installation Context${NC}"
    echo ""

    print_info "Source: ${CYAN}$REPO_ROOT${NC}"
    print_info "Target: ${CYAN}$TARGET_DIR${NC}"
    print_info "Edition: ${CYAN}$PROFILE${NC}"
    print_info "Language: ${CYAN}$LANGUAGE${NC}"
    echo ""
}

verify_source_files() {
    local missing=0

    echo -e "  ${BOLD}Verifying source files...${NC}"
    echo ""

    local required_paths=(
        "install/shared"
        "install/skills"
        "install/agents"
        "install/workspace/skills"
        "install/settings"
        "install/claude-md"
        "install/profiles"
        "help"
    )

    for path in "${required_paths[@]}"; do
        if [ -e "$REPO_ROOT/$path" ]; then
            print_success "$path"
        else
            print_error "$path ${DIM}(missing)${NC}"
            missing=$((missing + 1))
        fi
    done

    echo ""

    if [ $missing -gt 0 ]; then
        print_error "Source directory is incomplete!"
        echo ""
        echo -e "  ${DIM}Expected shipkit structure at: $REPO_ROOT${NC}"
        echo ""
        return 1
    fi

    return 0
}

check_project_root() {
    if [ -d ".git" ]; then
        return 0
    else
        return 1
    fi
}

confirm() {
    local prompt="$1"
    local default="${2:-y}"

    if [ "$default" = "y" ]; then
        local hint="Y/n"
    else
        local hint="y/N"
    fi

    echo -ne "  ${BOLD}${prompt}${NC} ${DIM}[${hint}]${NC} "
    read -r response

    if [ -z "$response" ]; then
        response="$default"
    fi

    [[ "$response" =~ ^[Yy] ]]
}

open_html_docs() {
    local html_dir="$REPO_ROOT/help"

    echo ""
    echo -e "  ${BRIGHT_CYAN}📖 Opening documentation...${NC}"
    echo ""

    if [ ! -d "$html_dir" ]; then
        print_warning "Documentation files not found in $html_dir"
        return 1
    fi

    # Choose appropriate overview based on edition
    local overview_file
    if [ "$PROFILE" = "lite" ]; then
        overview_file="$html_dir/shipkit-lite-overview.html"
    else
        overview_file="$html_dir/system-overview.html"
    fi

    if [ ! -f "$overview_file" ]; then
        print_warning "Overview not found: $overview_file"
        return 1
    fi

    # Detect OS and open overview
    local overview_name=$(basename "$overview_file")
    case "$(uname -s)" in
        Darwin*)
            open "$overview_file" 2>/dev/null && print_success "Opened $overview_name" || print_warning "Could not open $overview_name"
            ;;
        Linux*)
            if command -v xdg-open &> /dev/null; then
                xdg-open "$overview_file" 2>/dev/null && print_success "Opened $overview_name"
            else
                print_warning "xdg-open not found. View docs at: $html_dir"
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            start "$overview_file" 2>/dev/null && print_success "Opened $overview_name" || print_warning "Could not open $overview_name"
            ;;
        *)
            print_warning "Unknown OS. View docs at: $html_dir"
            ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

install_shared_core() {
    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Installing shared core files${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Install hooks (edition-specific)
    print_info "Installing session hooks..."
    mkdir -p .claude/hooks

    if [ "$PROFILE" = "lite" ]; then
        # Install lite-specific hooks
        cp "$REPO_ROOT/install/shared/hooks/lite-session-start.py" .claude/hooks/session-start.py
        cp "$REPO_ROOT/install/shared/hooks/lite-suggest-next-skill.py" .claude/hooks/suggest-next-skill.py
        print_success "Installed session hooks (lite edition)"
    else
        # Install full Shipkit hooks
        cp "$REPO_ROOT/install/shared/hooks/session-start.py" .claude/hooks/session-start.py
        cp "$REPO_ROOT/install/shared/hooks/suggest-next-skill.py" .claude/hooks/suggest-next-skill.py
        print_success "Installed session hooks (full edition)"
    fi

    chmod +x .claude/hooks/*.py 2>/dev/null || true

    # Install scripts
    print_info "Installing shared scripts..."
    mkdir -p .shipkit/scripts/bash
    mkdir -p .shipkit/scripts/python
    cp "$REPO_ROOT/install/shared/scripts/bash/"* .shipkit/scripts/bash/ 2>/dev/null || true
    cp "$REPO_ROOT/install/shared/scripts/python/"* .shipkit/scripts/python/ 2>/dev/null || true
    chmod +x .shipkit/scripts/bash/*.sh 2>/dev/null || true
    print_success "Installed shared scripts"

    # Install git files
    print_info "Installing git configuration files..."

    if [ ! -f ".gitignore" ]; then
        cp "$REPO_ROOT/install/shared/.gitignore" ./.gitignore 2>/dev/null || true
        print_success "Installed .gitignore"
    else
        print_warning ".gitignore exists, skipping"
    fi

    # No longer install .gitattributes - hooks are Python now (no line ending issues)
}

install_edition_files() {
    echo ""
    echo -e "  ${BOLD}Installing edition-specific files${NC}"
    echo ""

    # Install settings.json
    print_info "Installing settings.json for ${PROFILE} edition..."
    mkdir -p .claude
    local settings_source="$REPO_ROOT/install/settings/$MANIFEST_SETTINGS_FILE"

    if [ ! -f ".claude/settings.json" ]; then
        cp "$settings_source" .claude/settings.json
        print_success "Installed settings.json"
    else
        print_warning "settings.json exists, preserving your custom config"
    fi

    # Install CLAUDE.md
    print_info "Installing CLAUDE.md for ${PROFILE} edition..."
    local claude_md_source="$REPO_ROOT/install/claude-md/$MANIFEST_CLAUDE_MD_FILE"

    if [ ! -f "CLAUDE.md" ]; then
        cp "$claude_md_source" ./CLAUDE.md
        print_success "Installed CLAUDE.md"
    else
        print_warning "CLAUDE.md exists, skipping"
    fi
}

install_skills() {
    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Installing skills${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    mkdir -p .claude/skills
    mkdir -p .shipkit/skills

    # Install skill definitions
    print_info "Installing skill definitions..."
    local def_count=0
    for skill in "${MANIFEST_SKILLS_DEFINITIONS[@]}"; do
        if [ -n "$skill" ] && [ -d "$REPO_ROOT/install/skills/$skill" ]; then
            cp -r "$REPO_ROOT/install/skills/$skill" .claude/skills/
            def_count=$((def_count + 1))
        fi
    done
    print_success "Installed $def_count skill definitions"

    # Install skill implementations (workspace)
    print_info "Installing skill implementations..."
    local impl_count=0
    for skill in "${MANIFEST_SKILLS_WORKSPACE[@]}"; do
        if [ -n "$skill" ] && [ -d "$REPO_ROOT/install/workspace/skills/$skill" ]; then
            mkdir -p ".shipkit/skills/$skill"

            # Copy scripts, templates, references
            [ -d "$REPO_ROOT/install/workspace/skills/$skill/scripts" ] && \
                cp -r "$REPO_ROOT/install/workspace/skills/$skill/scripts" ".shipkit/skills/$skill/"
            [ -d "$REPO_ROOT/install/workspace/skills/$skill/templates" ] && \
                cp -r "$REPO_ROOT/install/workspace/skills/$skill/templates" ".shipkit/skills/$skill/"
            [ -d "$REPO_ROOT/install/workspace/skills/$skill/references" ] && \
                cp -r "$REPO_ROOT/install/workspace/skills/$skill/references" ".shipkit/skills/$skill/"

            # Create empty outputs folder
            mkdir -p ".shipkit/skills/$skill/outputs"

            impl_count=$((impl_count + 1))
        fi
    done
    print_success "Installed $impl_count skill implementations"

    # Make scripts executable
    find .shipkit/skills -name "*.sh" -type f -exec chmod +x {} \; 2>/dev/null || true
}

install_agents() {
    echo ""
    echo -e "  ${BOLD}Installing agent personas${NC}"
    echo ""

    if [ ${#MANIFEST_AGENTS[@]} -eq 0 ]; then
        print_info "No agents in manifest, skipping"
        return 0
    fi

    mkdir -p .claude/agents

    local count=0
    for agent in "${MANIFEST_AGENTS[@]}"; do
        if [ -n "$agent" ] && [ -f "$REPO_ROOT/install/agents/${agent}.md" ]; then
            cp "$REPO_ROOT/install/agents/${agent}.md" .claude/agents/
            count=$((count + 1))
        fi
    done

    print_success "Installed $count agent personas"
}

delete_unused_language() {
    echo ""
    echo -e "  ${BOLD}Removing unused language scripts${NC}"
    echo ""

    if [ "$LANGUAGE" = "bash" ]; then
        print_info "Removing Python scripts (.py files)..."
        find .shipkit/skills -name "*.py" -type f -delete 2>/dev/null || true
        find .shipkit/scripts/python -type f -delete 2>/dev/null || true
        print_success "Removed Python scripts"
    elif [ "$LANGUAGE" = "python" ]; then
        print_info "Removing Bash scripts (.sh files)..."
        find .shipkit/skills -name "*.sh" -type f -delete 2>/dev/null || true
        find .shipkit/scripts/bash -name "*.sh" -type f -delete 2>/dev/null || true
        print_success "Removed Bash scripts"
    fi
}

normalize_line_endings() {
    echo ""
    echo -e "  ${BOLD}Normalizing line endings${NC}"
    echo ""

    print_info "Converting hook scripts to Unix (LF) line endings..."

    local count=0
    for script in .claude/hooks/*.sh 2>/dev/null; do
        if [ -f "$script" ]; then
            tr -d '\r' < "$script" > "$script.tmp"
            mv "$script.tmp" "$script"
            chmod +x "$script"
            count=$((count + 1))
        fi
    done

    if [ $count -gt 0 ]; then
        print_success "Normalized $count hook scripts"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

show_completion() {
    local skill_count=$(find .claude/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    local agent_count=$(ls -1 .claude/agents/*.md 2>/dev/null | wc -l | tr -d ' ')
    local skill_impl_count=$(find .shipkit/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')

    echo ""
    echo ""
    echo -e "${BRIGHT_GREEN}"
    cat << 'EOF'
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ✓  Installation Complete!                               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    echo -e "  ${BOLD}What was installed:${NC}"
    echo ""
    print_success "Edition: ${CYAN}${PROFILE}${NC}"
    print_success "Language: ${CYAN}${LANGUAGE}${NC}"
    print_success "${skill_count} skill definitions (.claude/skills/)"
    print_success "${skill_impl_count} skill implementations (.shipkit/skills/)"

    if [ "$agent_count" -gt 0 ]; then
        print_success "${agent_count} agent personas (.claude/agents/)"
    fi

    print_success "Shared scripts (.shipkit/scripts/${LANGUAGE}/)"
    print_success "Session hooks (.claude/hooks/)"
    print_success "Settings (.claude/settings.json)"
    print_success "Project instructions (CLAUDE.md)"
    print_success "Git configuration (.gitignore)"

    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Next Steps${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "  ${CYAN}1.${NC} Start Claude Code in ${CYAN}$TARGET_DIR${NC}"
    echo ""

    if [ "$PROFILE" = "lite" ]; then
        echo -e "  ${CYAN}2.${NC} Quick Start (Lite Edition):"
        echo ""
        echo -e "     ${GREEN}/lite-project-context${NC} → ${GREEN}/lite-spec${NC}"
        echo -e "     → ${GREEN}/lite-plan${NC} → ${GREEN}/lite-implement${NC}"
        echo ""
    else
        echo -e "  ${CYAN}2.${NC} Choose your workflow:"
        echo ""
        echo -e "     ${DIM}Full product development:${NC}"
        echo -e "     ${GREEN}/prod-strategic-thinking${NC} → ${GREEN}/prod-constitution-builder${NC}"
        echo -e "     → ${GREEN}/prod-personas${NC} → ${GREEN}/prod-user-stories${NC}"
        echo ""
        echo -e "     ${DIM}Quick POC:${NC}"
        echo -e "     ${GREEN}/prod-constitution-builder${NC} → ${GREEN}/dev-specify${NC} → ${GREEN}/dev-implement${NC}"
        echo ""
    fi

    if [ "$PROFILE" = "lite" ]; then
        echo -e "  ${CYAN}3.${NC} Type ${GREEN}/lite-project-status${NC} to see current state"
    else
        echo -e "  ${CYAN}3.${NC} Type ${GREEN}/shipkit-status${NC} to see current state"
    fi
    echo ""
    echo -e "  ${DIM}Happy shipping! 🚀${NC}"
    echo ""

    # Open documentation in browser
    open_html_docs
}

# ═══════════════════════════════════════════════════════════════════════════════
# USAGE & CLI
# ═══════════════════════════════════════════════════════════════════════════════

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Install Shipkit framework into a target directory.

OPTIONS:
    --profile <lite|default>   Edition to install (default: prompts interactively)
    --language <bash|python>   Scripting language (default: prompts interactively)
    --target <path>            Target directory (default: prompts interactively)
    --yes, -y                  Skip confirmations
    --help                     Show this help

EXAMPLES:
    # Interactive mode (prompts for all options)
    bash install.sh

    # Install lite edition with Python to current directory
    bash install.sh --profile=lite --language=python -y

    # Install default edition with Bash to specific directory
    bash install.sh --profile=default --language=bash --target=/path/to/project

    # Install to specific directory (interactive prompts for profile/language)
    bash install.sh --target ~/my-project

EDITIONS:
    lite      - Fast, minimal (7 skills, POCs and side projects)
    default   - Complete (24 skills, full product development)

LANGUAGES:
    bash      - Traditional shell scripts (cross-platform)
    python    - Python scripts (recommended for Windows)

WHAT GETS INSTALLED:
    .claude/
      skills/           Skill definitions (SKILL.md files)
      agents/           Agent personas (if any in manifest)
      hooks/            Session start hooks
      settings.json     Edition-specific settings

    .shipkit/
      skills/           Skill implementations
        */scripts/      Automation (in selected language)
        */templates/    Templates
        */references/   Extended docs
        */outputs/      Empty (populated when skills run)
      scripts/
        bash/ or python/  Shared utilities

    CLAUDE.md           Edition-specific project instructions
    .gitignore          Git ignore file

EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --profile=*) PROFILE="${1#*=}"; shift;;
            --profile) PROFILE="$2"; shift 2;;
            --language=*) LANGUAGE="${1#*=}"; shift;;
            --language) LANGUAGE="$2"; shift 2;;
            --target=*) TARGET_DIR="${1#*=}"; shift;;
            --target) TARGET_DIR="$2"; shift 2;;
            --yes|-y) INTERACTIVE=false; shift;;
            --help) show_usage; exit 0;;
            --*) echo "Unknown option: $1"; show_usage; exit 1;;
            *)
                echo "Unknown argument: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Check for Python (required for manifest parsing)
    if ! command -v python3 &> /dev/null; then
        print_error "python3 is required but not found in PATH"
        echo ""
        echo "Please install Python 3 and try again."
        exit 1
    fi

    # Prompt for profile if not specified
    if [ -z "$PROFILE" ]; then
        if [ "$INTERACTIVE" = true ]; then
            clear_screen
            show_logo
            prompt_for_profile
        else
            print_error "Profile not specified. Use --profile=lite or --profile=default"
            exit 1
        fi
    fi

    # Validate profile
    if [ "$PROFILE" != "lite" ] && [ "$PROFILE" != "default" ]; then
        print_error "Invalid profile: $PROFILE. Must be 'lite' or 'default'"
        exit 1
    fi

    # Prompt for language if not specified
    if [ -z "$LANGUAGE" ]; then
        if [ "$INTERACTIVE" = true ]; then
            prompt_for_language
        else
            print_error "Language not specified. Use --language=bash or --language=python"
            exit 1
        fi
    fi

    # Validate language
    if [ "$LANGUAGE" != "bash" ] && [ "$LANGUAGE" != "python" ]; then
        print_error "Invalid language: $LANGUAGE. Must be 'bash' or 'python'"
        exit 1
    fi

    # Load manifest
    load_manifest "$PROFILE"

    # Prompt for directory if not specified
    if [ -z "$TARGET_DIR" ]; then
        if [ "$INTERACTIVE" = true ]; then
            prompt_for_directory
        else
            TARGET_DIR="$PWD"
        fi
    fi

    # Convert to absolute path
    if [[ "$TARGET_DIR" != /* ]] && [[ ! "$TARGET_DIR" =~ ^[A-Za-z]:[/\\] ]]; then
        TARGET_DIR="$PWD/$TARGET_DIR"
    fi

    # Create target directory if it doesn't exist
    if [ ! -d "$TARGET_DIR" ]; then
        if [ "$INTERACTIVE" = true ]; then
            echo ""
            if ! confirm "Target directory ${CYAN}$TARGET_DIR${NC} doesn't exist. Create it?"; then
                print_info "Installation cancelled."
                exit 0
            fi
        fi
        mkdir -p "$TARGET_DIR" || {
            print_error "Failed to create directory: $TARGET_DIR"
            exit 1
        }
    fi

    # Change to target directory
    cd "$TARGET_DIR" || {
        print_error "Failed to access directory: $TARGET_DIR"
        exit 1
    }

    # Show logo if not already shown
    if [ "$INTERACTIVE" = true ] && [ -n "$LANGUAGE" ]; then
        clear_screen
        show_logo "$PROFILE"
    elif [ "$INTERACTIVE" = false ]; then
        show_mini_logo
    fi

    # Detect and verify
    detect_installation_context

    if ! verify_source_files; then
        exit 1
    fi

    # Check project root
    if ! check_project_root; then
        echo ""
        print_warning "No .git directory found. This might not be a project root."
        if [ "$INTERACTIVE" = true ]; then
            if ! confirm "Continue anyway?"; then
                print_info "Installation cancelled."
                exit 0
            fi
        fi
    fi

    # Confirm installation location
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        if ! confirm "Install Shipkit ${PROFILE} edition to ${CYAN}$TARGET_DIR${NC}?"; then
            print_info "Installation cancelled."
            exit 0
        fi
    fi

    # Perform installation
    echo ""
    print_info "Installing Shipkit framework..."

    install_shared_core
    install_edition_files
    install_skills
    install_agents
    delete_unused_language
    normalize_line_endings

    # Show completion
    show_completion
}

# Run main
main "$@"
