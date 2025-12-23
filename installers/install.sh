#!/usr/bin/env bash
# install.sh - Shipkit Installer
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
INTERACTIVE=true
GITHUB_URL=""
GITHUB_BRANCH="main"
TEMP_DIR=""
CLEANUP_TEMP=false

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
# ASCII ART HEADER
# ═══════════════════════════════════════════════════════════════════════════════

show_logo() {
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
    echo -e "${DIM}         Complete Product Development Framework${NC}"
    echo -e "${DIM}              24 Skills • 6 Agents • Constitution-Driven${NC}"
    echo ""
}

show_mini_logo() {
    echo ""
    echo -e "${BRIGHT_MAGENTA}  ╭──────────────────────────────────────╮${NC}"
    echo -e "${BRIGHT_MAGENTA}  │${NC}  ${BOLD}ShipKit${NC} ${DIM}• 24 Skills${NC}                ${BRIGHT_MAGENTA}│${NC}"
    echo -e "${BRIGHT_MAGENTA}  ╰──────────────────────────────────────╯${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

detect_installation_context() {
    echo -e "  ${BOLD}Detecting installation context...${NC}"
    echo ""

    print_info "Source: ${CYAN}$SCRIPT_DIR${NC}"
    print_info "Target: ${CYAN}$TARGET_DIR${NC}"
    echo ""
}

verify_source_files() {
    local missing=0

    echo -e "  ${BOLD}Verifying source files...${NC}"
    echo ""

    local required_paths=(
        "install/skills"
        "install/agents"
        "install/workspace/skills"
        "install/workspace/scripts"
        "install/hooks"
        "install/settings.json"
        "install/CLAUDE.md"
        "install/.gitignore"
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
    # Check for Unix absolute path (starts with /) OR Windows absolute path (e.g., C:\, P:\, /c/, /p/)
    if [[ "$TARGET_DIR" != /* ]] && [[ ! "$TARGET_DIR" =~ ^[A-Za-z]:[/\\] ]]; then
        TARGET_DIR="$PWD/$TARGET_DIR"
    fi
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

    local skills_summary="$html_dir/skills-summary.html"
    local system_overview="$html_dir/system-overview.html"

    # Detect OS and open files
    case "$(uname -s)" in
        Darwin*)
            # macOS
            if [ -f "$system_overview" ]; then
                open "$system_overview" 2>/dev/null && print_success "Opened system-overview.html" || print_warning "Could not open system-overview.html"
            fi
            if [ -f "$skills_summary" ]; then
                open "$skills_summary" 2>/dev/null && print_success "Opened skills-summary.html" || print_warning "Could not open skills-summary.html"
            fi
            ;;
        Linux*)
            # Linux
            if command -v xdg-open &> /dev/null; then
                [ -f "$system_overview" ] && xdg-open "$system_overview" 2>/dev/null && print_success "Opened system-overview.html"
                [ -f "$skills_summary" ] && xdg-open "$skills_summary" 2>/dev/null && print_success "Opened skills-summary.html"
            else
                print_warning "xdg-open not found. View docs at: $html_dir"
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            # Windows (Git Bash, MSYS2, Cygwin)
            if [ -f "$system_overview" ]; then
                start "$system_overview" 2>/dev/null && print_success "Opened system-overview.html" || print_warning "Could not open system-overview.html"
            fi
            if [ -f "$skills_summary" ]; then
                start "$skills_summary" 2>/dev/null && print_success "Opened skills-summary.html" || print_warning "Could not open skills-summary.html"
            fi
            ;;
        *)
            print_warning "Unknown OS. View docs at: $html_dir"
            ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

install_skills() {
    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Installing skills${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    mkdir -p .claude/skills

    print_loading "Installing skill definitions"
    cp -r "$REPO_ROOT/install/skills/"* .claude/skills/

    local skill_count=$(find .claude/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    print_success "Installed $skill_count skill definitions"
    print_bullet "12 product skills (prod-*)"
    print_bullet "9 development skills (dev-*)"
    print_bullet "3 meta skills (shipkit-master, dev-discussion, dev-writing-skills)"
}

install_agents() {
    echo ""
    echo -e "  ${BOLD}Installing agent personas${NC}"
    echo ""

    print_info "Creating .claude/agents directory..."
    mkdir -p .claude/agents

    local count=0
    print_info "Copying agent files from $REPO_ROOT/install/agents..."
    for agent in "$REPO_ROOT/install/agents"/*.md; do
        if [ -f "$agent" ]; then
            filename=$(basename "$agent")
            # Skip README.md - it's documentation, not an agent definition
            if [ "$filename" = "README.md" ]; then
                print_info "  Skipping README.md (documentation only)"
                continue
            fi
            print_info "  Checking $filename..."
            if [ ! -f ".claude/agents/$filename" ]; then
                print_info "    Copying $filename..."
                cp "$agent" .claude/agents/
                count=$((count + 1))
            else
                print_info "    Skipping $filename (already exists)"
            fi
        fi
    done

    print_success "Installed $count agent personas"
    print_bullet "prod-product-manager, prod-product-designer"
    print_bullet "dev-architect, dev-implementer, dev-reviewer"
    print_bullet "any-researcher"
}

install_hooks() {
    echo ""
    echo -e "  ${BOLD}Installing session hooks${NC}"
    echo ""

    print_info "Creating .claude/hooks directory..."
    mkdir -p .claude/hooks

    print_info "Copying hook files from $REPO_ROOT/install/hooks..."
    # Copy all hook files
    for file in "$REPO_ROOT/install/hooks/"*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            print_info "  Copying $filename..."
            cp "$file" .claude/hooks/
        fi
    done

    print_info "Making hook scripts executable..."
    chmod +x .claude/hooks/*.sh 2>/dev/null || true

    print_success "Installed session hooks"
    print_bullet "SessionStart hook loads shipkit-master"
}

install_settings() {
    echo ""
    echo -e "  ${BOLD}Installing settings.json${NC}"
    echo ""

    SETTINGS_FILE=".claude/settings.json"

    print_info "Checking if settings.json already exists..."
    if [ ! -f "$SETTINGS_FILE" ]; then
        print_info "No existing settings.json found"
        if [ -f "$REPO_ROOT/install/settings.json" ]; then
            print_info "Copying settings.json from $REPO_ROOT/install/settings.json..."
            cp "$REPO_ROOT/install/settings.json" "$SETTINGS_FILE"
            print_success "Installed settings.json"
            print_bullet "File protections: .claude/* and .shipkit/skills/*/outputs|templates|scripts"
            print_bullet "SessionStart hook configured"
            print_bullet "SkillComplete prompts enabled"
        else
            print_error "Source settings.json not found!"
            return 1
        fi
    else
        print_warning "settings.json exists, preserving your custom config"
        print_info "Backup your settings before re-installing if needed"
    fi
}

install_workspace() {
    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Setting up workspace${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    print_info "Creating .shipkit/ workspace structure..."
    # Create base directories
    mkdir -p .shipkit/scripts
    mkdir -p .shipkit/skills
    print_success "Created .shipkit base directories"

    # Copy shared scripts
    print_info "Copying shared scripts from $REPO_ROOT/install/workspace/scripts/bash..."
    if [ -d "$REPO_ROOT/install/workspace/scripts/bash" ]; then
        cp -r "$REPO_ROOT/install/workspace/scripts/bash" .shipkit/scripts/
        chmod +x .shipkit/scripts/bash/*.sh 2>/dev/null || true
        print_success "Installed shared scripts (common.sh)"
    else
        print_warning "Shared scripts directory not found, skipping"
    fi

    # Copy all skill implementations
    print_info "Installing skill implementations (scripts, templates, references)..."

    local skill_impl_count=0
    if [ -d "$REPO_ROOT/install/workspace/skills" ]; then
        for skill_dir in "$REPO_ROOT/install/workspace/skills/"*/; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                print_info "  Processing skill: $skill_name..."
                mkdir -p ".shipkit/skills/$skill_name"

                # Copy scripts, templates, references
                if [ -d "$skill_dir/scripts" ]; then
                    print_info "    Copying scripts..."
                    cp -r "$skill_dir/scripts" ".shipkit/skills/$skill_name/"
                fi
                if [ -d "$skill_dir/templates" ]; then
                    print_info "    Copying templates..."
                    cp -r "$skill_dir/templates" ".shipkit/skills/$skill_name/"
                fi
                if [ -d "$skill_dir/references" ]; then
                    print_info "    Copying references..."
                    cp -r "$skill_dir/references" ".shipkit/skills/$skill_name/"
                fi

                # Create empty outputs folder (will be populated by skills)
                print_info "    Creating outputs directory..."
                mkdir -p ".shipkit/skills/$skill_name/outputs"

                skill_impl_count=$((skill_impl_count + 1))
                print_info "    ✓ $skill_name complete"
            fi
        done
    else
        print_error "Workspace skills directory not found!"
        return 1
    fi

    print_success "Installed $skill_impl_count skill implementations"
    print_bullet "Scripts: Automation for each skill"
    print_bullet "Templates: Single adaptive template per skill"
    print_bullet "References: Extended docs, examples, patterns"
    print_bullet "Outputs: Empty (populated when skills run)"

    # Make skill scripts executable
    find .shipkit/skills -name "*.sh" -type f -exec chmod +x {} \; 2>/dev/null || true

    echo ""
    print_success "Shipkit workspace ready"
    print_bullet "Unified .shipkit/ structure for all skills"
}

install_claude_md() {
    echo ""
    echo -e "  ${BOLD}Installing CLAUDE.md${NC}"
    echo ""

    print_info "Checking if CLAUDE.md already exists..."
    if [ ! -f "CLAUDE.md" ]; then
        print_info "No existing CLAUDE.md found"
        if [ -f "$REPO_ROOT/install/CLAUDE.md" ]; then
            print_info "Copying CLAUDE.md from $REPO_ROOT/install/CLAUDE.md..."
            cp "$REPO_ROOT/install/CLAUDE.md" ./CLAUDE.md
            print_success "Installed CLAUDE.md (project instructions)"
            print_bullet "24 skill routing guide"
            print_bullet "Constitution-driven workflows"
            print_bullet "Product → Development integration"
        else
            print_error "Source CLAUDE.md not found at $REPO_ROOT/install/CLAUDE.md!"
            return 1
        fi
    else
        print_warning "CLAUDE.md exists, skipping"
        print_info "Delete existing CLAUDE.md if you want to reinstall"
    fi
}

install_gitignore() {
    echo ""
    echo -e "  ${BOLD}Installing .gitignore${NC}"
    echo ""

    print_info "Checking if .gitignore already exists..."
    if [ ! -f ".gitignore" ]; then
        print_info "No existing .gitignore found"
        if [ -f "$REPO_ROOT/install/.gitignore" ]; then
            print_info "Copying .gitignore from $REPO_ROOT/install/.gitignore..."
            cp "$REPO_ROOT/install/.gitignore" ./.gitignore
            print_success "Installed .gitignore"
            print_bullet "Excludes .claude/, .shipkit/, CLAUDE.md"
            print_bullet "Excludes env files and common IDE folders"
        else
            print_warning "Source .gitignore not found, skipping"
        fi
    else
        print_warning ".gitignore exists, skipping automatic install"
        print_info "Add these entries to your .gitignore manually:"
        print_bullet ".claude/"
        print_bullet ".shipkit/"
        print_bullet "CLAUDE.md"
    fi
}

install_gitattributes() {
    echo ""
    echo -e "  ${BOLD}Installing .gitattributes${NC}"
    echo ""

    print_info "Checking if .gitattributes already exists..."
    if [ ! -f ".gitattributes" ]; then
        print_info "No existing .gitattributes found"
        if [ -f "$REPO_ROOT/install/.gitattributes" ]; then
            print_info "Copying .gitattributes from $REPO_ROOT/install/.gitattributes..."
            cp "$REPO_ROOT/install/.gitattributes" ./.gitattributes
            print_success "Installed .gitattributes"
            print_bullet "Forces LF line endings for shell scripts"
            print_bullet "Protects .claude/hooks from Git autocrlf"
        else
            print_warning "Source .gitattributes not found, skipping"
        fi
    else
        # Check if existing .gitattributes has shell script rules
        if grep -q "\.sh.*eol=lf" .gitattributes 2>/dev/null; then
            print_success ".gitattributes exists with shell script protection"
        else
            print_warning ".gitattributes exists but missing shell script rules"
            print_info "Consider adding to your .gitattributes:"
            print_bullet "*.sh text eol=lf"
            print_bullet ".claude/hooks/* text eol=lf"
        fi
    fi
}

normalize_line_endings() {
    echo ""
    echo -e "  ${BOLD}Normalizing line endings${NC}"
    echo ""

    print_info "Converting hook scripts to Unix (LF) line endings..."

    local count=0
    for script in .claude/hooks/*.sh; do
        if [ -f "$script" ]; then
            # Remove carriage returns (CRLF → LF)
            tr -d '\r' < "$script" > "$script.tmp"
            mv "$script.tmp" "$script"
            chmod +x "$script"
            count=$((count + 1))
        fi
    done

    print_success "Normalized $count hook scripts"
    print_bullet "All hooks now have Unix (LF) line endings"
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
    print_success "${skill_count} skill definitions (.claude/skills/)"
    print_success "${skill_impl_count} skill implementations (.shipkit/skills/)"
    print_success "${agent_count} agent personas (.claude/agents/)"
    print_success "Shared scripts (.shipkit/scripts/bash/common.sh)"
    print_success "Session hooks (.claude/hooks/)"
    print_success "Settings with file protections (.claude/settings.json)"
    print_success "Project instructions (CLAUDE.md)"
    print_success "Git ignore file (.gitignore)"

    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Next Steps${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "  ${CYAN}1.${NC} Start Claude Code in ${CYAN}$TARGET_DIR${NC}"
    echo ""
    echo -e "  ${CYAN}2.${NC} Choose your workflow:"
    echo ""
    echo -e "     ${DIM}Full product development (Greenfield):${NC}"
    echo -e "     ${GREEN}/prod-strategic-thinking${NC} → ${GREEN}/prod-constitution-builder${NC}"
    echo -e "     → ${GREEN}/prod-personas${NC} → ${GREEN}/prod-user-stories${NC} → ${GREEN}/dev-specify${NC}"
    echo ""
    echo -e "     ${DIM}Quick POC (Fast validation):${NC}"
    echo -e "     ${GREEN}/prod-constitution-builder${NC} ${DIM}(choose POC)${NC} → ${GREEN}/dev-specify${NC} → ${GREEN}/dev-implement${NC}"
    echo ""
    echo -e "     ${DIM}Existing codebase (Add feature):${NC}"
    echo -e "     ${GREEN}/dev-constitution${NC} → ${GREEN}/dev-specify${NC} → ${GREEN}/dev-implement${NC}"
    echo ""
    echo -e "  ${CYAN}3.${NC} Type ${GREEN}/help${NC} to see all 24 skills"
    echo ""
    echo -e "  ${BRIGHT_CYAN}💡 Constitution-Driven Development:${NC}"
    echo -e "     Run ${GREEN}/prod-constitution-builder${NC} to choose project type:"
    echo -e "     ${DIM}• B2B/B2C Greenfield (comprehensive)${NC}"
    echo -e "     ${DIM}• Side Project MVP/POC (minimal)${NC}"
    echo -e "     ${DIM}• Experimental (learning-focused)${NC}"
    echo -e "     ${DIM}• Existing Project (document current state)${NC}"
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
Usage: $0 [TARGET_DIR] [OPTIONS]

Install Shipkit framework into a target directory.

ARGUMENTS:
    TARGET_DIR                 Target directory (optional, defaults to current directory)

OPTIONS:
    --target <path>            Target directory (alternative to positional argument)
    --github <URL>             Clone from GitHub instead of local
    --branch <name>            GitHub branch (default: main)
    --yes, -y                  Skip confirmations
    --help                     Show this help

EXAMPLES:
    # Interactive mode in current directory
    bash install.sh

    # Install to specific directory (positional)
    bash install.sh /path/to/project

    # Install to specific directory (flag)
    bash install.sh --target /path/to/project

    # Non-interactive installation
    bash install.sh /path/to/project -y

    # From GitHub to specific directory
    bash install.sh --target ~/my-project --github https://github.com/user/shipkit.git

WHAT GETS INSTALLED:
    .claude/
      skills/           24 skill definitions (SKILL.md files)
      agents/           6 agent personas
      hooks/            Session start hooks
      settings.json     Permissions and file protections

    .shipkit/
      skills/           24 skill implementations
        */scripts/      Automation for each skill
        */templates/    Templates (including 6 constitution templates)
        */references/   Extended docs and examples
        */outputs/      Empty (populated when skills run)
      scripts/
        bash/common.sh  Shared utilities

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

EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --target) TARGET_DIR="$2"; shift 2;;
            --github) GITHUB_URL="$2"; shift 2;;
            --branch) GITHUB_BRANCH="$2"; shift 2;;
            --yes|-y) INTERACTIVE=false; shift;;
            --help) show_usage; exit 0;;
            --*) echo "Unknown option: $1"; show_usage; exit 1;;
            *)
                # Positional argument - treat as target directory
                if [ -z "$TARGET_DIR" ]; then
                    TARGET_DIR="$1"
                    shift
                else
                    echo "Error: Multiple target directories specified"
                    show_usage
                    exit 1
                fi
                ;;
        esac
    done

    # Prompt for directory in interactive mode if not specified
    if [ -z "$TARGET_DIR" ]; then
        if [ "$INTERACTIVE" = true ] && [ -z "$GITHUB_URL" ]; then
            prompt_for_directory
        else
            TARGET_DIR="$PWD"
        fi
    fi

    # Convert to absolute path
    # Check for Unix absolute path (starts with /) OR Windows absolute path (e.g., C:\, P:\, /c/, /p/)
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

    # Handle GitHub mode
    if [ -n "$GITHUB_URL" ]; then
        show_mini_logo
        print_info "Cloning from GitHub..."
        print_bullet "URL: $GITHUB_URL"
        print_bullet "Branch: $GITHUB_BRANCH"
        echo ""

        if ! command -v git &> /dev/null; then
            print_error "git is not installed"
            exit 1
        fi

        TEMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'shipkit')
        CLEANUP_TEMP=true

        if git clone --depth 1 --branch "$GITHUB_BRANCH" "$GITHUB_URL" "$TEMP_DIR" 2>&1; then
            print_success "Repository cloned"
            SCRIPT_DIR="$TEMP_DIR"
        else
            print_error "Failed to clone repository"
            echo ""
            print_warning "Common causes:"
            print_bullet "Repository is private (requires authentication)"
            print_bullet "Invalid URL or branch name"
            print_bullet "Network connectivity issues"
            echo ""
            print_info "For private repos, clone manually first:"
            echo -e "  ${DIM}git clone $GITHUB_URL /your/path${NC}"
            echo -e "  ${DIM}cd /your/path${NC}"
            echo -e "  ${DIM}bash install.sh${NC}"
            echo ""
            exit 1
        fi
        echo ""
    fi

    # Show logo
    if [ "$INTERACTIVE" = true ]; then
        clear_screen
    fi
    show_logo

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
        if ! confirm "Install Shipkit to ${CYAN}$TARGET_DIR${NC}?"; then
            print_info "Installation cancelled."
            exit 0
        fi
    fi

    # Perform installation
    echo ""
    print_info "Installing Shipkit framework..."

    install_skills
    install_agents
    install_hooks
    install_settings
    install_workspace
    install_claude_md
    install_gitignore
    install_gitattributes
    normalize_line_endings

    # Show completion
    show_completion
}

# Run main
main "$@"
