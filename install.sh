#!/usr/bin/env bash
# install.sh - Interactive ShipKit Installer
set -e

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS & STYLING
# ═══════════════════════════════════════════════════════════════════════════════

BOLD='\033[1m'
DIM='\033[2m'
ITALIC='\033[3m'
UNDERLINE='\033[4m'
RESET='\033[0m'

# Colors
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'

# Bright colors
BRIGHT_GREEN='\033[1;32m'
BRIGHT_BLUE='\033[1;34m'
BRIGHT_CYAN='\033[1;36m'
BRIGHT_MAGENTA='\033[1;35m'
BRIGHT_WHITE='\033[1;37m'

# Background
BG_BLUE='\033[44m'
BG_MAGENTA='\033[45m'

NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR=".claude/skills"
PRESET=""
GITHUB_URL=""
GITHUB_BRANCH="main"
TEMP_DIR=""
CLEANUP_TEMP=false
INTERACTIVE=true

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

# Print centered text
print_centered() {
    local text="$1"
    local width=60
    local padding=$(( (width - ${#text}) / 2 ))
    printf "%${padding}s%s\n" "" "$text"
}

# Animated dots
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
    │   ███████╗██╗  ██╗██╗██████╗ ██╗  ██╗██╗████████╗      /  \           │
    │   ██╔════╝██║  ██║██║██╔══██╗██║ ██╔╝██║╚══██╔══╝     / /| \          │
    │   ███████╗███████║██║██████╔╝█████╔╝ ██║   ██║       / / |  \         │
    │   ╚════██║██╔══██║██║██╔═══╝ ██╔═██╗ ██║   ██║      /_/__|___\        │
    │   ███████║██║  ██║██║██║     ██║  ██╗██║   ██║      \________/        │
    │   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝      ~~~~~~~~~~        │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘
EOF
    echo -e "${NC}"
    echo -e "${DIM}              Complete Product Development Framework${NC}"
    echo -e "${DIM}                  ProdKit + DevKit + Agents${NC}"
    echo ""
}

show_mini_logo() {
    echo ""
    echo -e "${BRIGHT_MAGENTA}  ╭──────────────────────────────────────╮${NC}"
    echo -e "${BRIGHT_MAGENTA}  │${NC}  ${BOLD}ShipKit${NC} ${DIM}• Product → Code${NC}            ${BRIGHT_MAGENTA}│${NC}"
    echo -e "${BRIGHT_MAGENTA}  ╰──────────────────────────────────────╯${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE MENU FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Generic selection menu
# Usage: select_option "prompt" "option1" "option2" ...
# Returns: selected index (0-based) in $SELECTED_INDEX
select_option() {
    local prompt="$1"
    shift
    local options=("$@")
    local selected=0
    local key=""

    # Hide cursor
    tput civis 2>/dev/null || true

    while true; do
        # Clear and redraw menu
        echo -e "\n  ${BOLD}${prompt}${NC}\n"

        for i in "${!options[@]}"; do
            if [ $i -eq $selected ]; then
                echo -e "  ${BRIGHT_CYAN}❯${NC} ${BRIGHT_WHITE}${options[$i]}${NC}"
            else
                echo -e "    ${DIM}${options[$i]}${NC}"
            fi
        done

        echo -e "\n  ${DIM}↑/↓ to move, Enter to select${NC}"

        # Read single keypress
        read -rsn1 key

        # Handle arrow keys (they send escape sequences)
        if [[ $key == $'\x1b' ]]; then
            read -rsn2 key
            case $key in
                '[A') # Up arrow
                    ((selected--))
                    [ $selected -lt 0 ] && selected=$((${#options[@]} - 1))
                    ;;
                '[B') # Down arrow
                    ((selected++))
                    [ $selected -ge ${#options[@]} ] && selected=0
                    ;;
            esac
        elif [[ $key == "" ]]; then
            # Enter pressed
            break
        fi

        # Move cursor up to redraw
        local lines=$((${#options[@]} + 4))
        tput cuu $lines 2>/dev/null || printf "\033[${lines}A"
        tput el 2>/dev/null || true
    done

    # Show cursor
    tput cnorm 2>/dev/null || true

    SELECTED_INDEX=$selected
}

# Yes/No confirmation
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

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

detect_installation_context() {
    echo -e "  ${BOLD}Detecting installation context...${NC}"
    echo ""

    # Get current directory name
    CURRENT_DIR=$(basename "$PWD")

    # Get source directory relative to current
    if [[ "$SCRIPT_DIR" == "$PWD"* ]]; then
        # Script is inside current directory
        REL_PATH=".${SCRIPT_DIR#$PWD}"
        INSTALL_METHOD="inside"
        DETECTED_MSG="ShipKit found ${UNDERLINE}inside${NC} your project"
    elif [[ "$SCRIPT_DIR" == "$(dirname "$PWD")"* ]]; then
        # Script is sibling to current directory
        REL_PATH="../$(basename "$SCRIPT_DIR")"
        INSTALL_METHOD="sibling"
        DETECTED_MSG="ShipKit found as ${UNDERLINE}sibling${NC} directory"
    else
        # Script is somewhere else
        REL_PATH="$SCRIPT_DIR"
        INSTALL_METHOD="external"
        DETECTED_MSG="ShipKit found at ${UNDERLINE}external${NC} location"
    fi

    print_info "$DETECTED_MSG"
    print_bullet "Source: ${CYAN}$SCRIPT_DIR${NC}"
    print_bullet "Target: ${CYAN}$PWD${NC}"
    echo ""
}

verify_source_files() {
    local missing=0

    echo -e "  ${BOLD}Verifying source files...${NC}"
    echo ""

    local dirs=("skills/devkit" "skills/prodkit" "skills/meta" "hooks" "devkit-files" "prodkit-files" "agents")

    for dir in "${dirs[@]}"; do
        if [ -d "$SCRIPT_DIR/$dir" ]; then
            print_success "$dir/"
        else
            print_error "$dir/ ${DIM}(missing)${NC}"
            ((missing++))
        fi
    done

    echo ""

    if [ $missing -gt 0 ]; then
        print_error "Source directory is incomplete!"
        echo ""
        echo -e "  ${DIM}Expected ShipKit structure at: $SCRIPT_DIR${NC}"
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

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE PRESET SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

show_preset_details() {
    echo ""
    echo -e "  ${BOLD}What's included in each preset:${NC}"
    echo ""
    echo -e "  ${BRIGHT_CYAN}Solo (Recommended)${NC}"
    print_bullet "DevKit: 23 skills (specs, implementation, TDD, reviews)"
    print_bullet "ProdKit: 11 skills (discovery, strategy, requirements)"
    print_bullet "Agent Personas: 5 specialized behaviors"
    print_bullet "Full infrastructure (.devkit/, .prodkit/)"
    echo ""
    echo -e "  ${CYAN}DevKit Only${NC}"
    print_bullet "DevKit: 23 skills + Agent Personas"
    print_bullet "For teams with existing product requirements"
    echo ""
    echo -e "  ${CYAN}ProdKit Only${NC}"
    print_bullet "ProdKit: 11 skills"
    print_bullet "For product discovery without technical specs"
    echo ""
}

select_preset_interactive() {
    echo -e "\n  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Choose your installation preset${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    select_option "Select a preset:" \
        "🚀 Solo (Recommended) - Full ShipKit: 34 skills + 5 agents" \
        "⚡ All/Team - Everything with advanced features" \
        "🔧 DevKit Only - Technical specs & development (23 skills)" \
        "📊 ProdKit Only - Product discovery (11 skills)" \
        "❓ Show me what's in each preset"

    case $SELECTED_INDEX in
        0) PRESET="solo" ;;
        1) PRESET="all" ;;
        2) PRESET="devkit-only" ;;
        3) PRESET="prodkit-only" ;;
        4)
            show_preset_details
            select_preset_interactive  # Recurse to show menu again
            return
            ;;
    esac

    echo ""
    print_success "Selected: ${BOLD}$PRESET${NC}"
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

    case $PRESET in
        all|team|solo)
            print_loading "Installing DevKit (23 skills)"
            cp -r "$SCRIPT_DIR/skills/devkit" .claude/skills/
            print_success "DevKit installed"

            print_loading "Installing ProdKit (11 skills)"
            cp -r "$SCRIPT_DIR/skills/prodkit" .claude/skills/
            print_success "ProdKit installed"

            INSTALL_DEVKIT=true
            INSTALL_PRODKIT=true
            ;;
        devkit-only)
            print_loading "Installing DevKit (23 skills)"
            cp -r "$SCRIPT_DIR/skills/devkit" .claude/skills/
            print_success "DevKit installed"
            INSTALL_DEVKIT=true
            INSTALL_PRODKIT=false
            ;;
        prodkit-only)
            print_loading "Installing ProdKit (11 skills)"
            cp -r "$SCRIPT_DIR/skills/prodkit" .claude/skills/
            print_success "ProdKit installed"
            INSTALL_DEVKIT=false
            INSTALL_PRODKIT=true
            ;;
    esac

    # Always install meta skill
    print_loading "Installing meta skill (enforcement)"
    mkdir -p .claude/skills/meta
    cp -r "$SCRIPT_DIR/skills/meta/"* .claude/skills/meta/
    print_success "Meta skill installed"
}

install_agents() {
    echo ""
    echo -e "  ${BOLD}Installing agent personas${NC}"
    echo ""

    mkdir -p .claude/agents

    local count=0
    for agent in "$SCRIPT_DIR/agents"/*.md; do
        if [ -f "$agent" ]; then
            filename=$(basename "$agent")
            if [ ! -f ".claude/agents/$filename" ]; then
                cp "$agent" .claude/agents/
                ((count++))
            fi
        fi
    done

    print_success "Installed $count agent personas"
    print_bullet "Discovery, Architect, Implementer, Reviewer, Researcher"
}

install_hooks() {
    echo ""
    echo -e "  ${BOLD}Installing session hooks${NC}"
    echo ""

    mkdir -p .claude/hooks
    cp -r "$SCRIPT_DIR/hooks/"* .claude/hooks/
    chmod +x .claude/hooks/*.sh 2>/dev/null || true

    # Configure settings.json
    SETTINGS_FILE=".claude/settings.json"
    if [ ! -f "$SETTINGS_FILE" ]; then
        cat > "$SETTINGS_FILE" << 'SETTINGS_EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "command": ".claude/hooks/run-hook.cmd session-start.sh"
      }
    ]
  }
}
SETTINGS_EOF
        print_success "Created settings.json with hooks"
    else
        print_warning "settings.json exists, hooks may need manual config"
    fi
}

install_infrastructure() {
    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Setting up infrastructure${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if [ "$INSTALL_DEVKIT" = true ]; then
        print_loading "Creating .devkit/ workspace"
        mkdir -p .devkit/scripts .devkit/templates .devkit/specs
        cp -r "$SCRIPT_DIR/devkit-files/scripts/bash" .devkit/scripts/
        cp -r "$SCRIPT_DIR/devkit-files/scripts/powershell" .devkit/scripts/ 2>/dev/null || true
        chmod +x .devkit/scripts/bash/*.sh 2>/dev/null || true
        cp "$SCRIPT_DIR/devkit-files/templates/"*.md .devkit/templates/ 2>/dev/null || true
        print_success "DevKit workspace ready"
    fi

    if [ "$INSTALL_PRODKIT" = true ]; then
        print_loading "Creating .prodkit/ workspace"
        mkdir -p .prodkit/scripts .prodkit/templates
        mkdir -p .prodkit/inputs/{strategy,personas,market,design,analytics,feedback}
        mkdir -p .prodkit/{strategy,discovery,brand,design,requirements,metrics,analysis,comms}
        cp -r "$SCRIPT_DIR/prodkit-files/scripts/bash" .prodkit/scripts/
        chmod +x .prodkit/scripts/bash/*.sh 2>/dev/null || true
        cp -r "$SCRIPT_DIR/prodkit-files/templates/"* .prodkit/templates/

        cat > .prodkit/README.md <<EOF
# ProdKit Workspace

Generated: $(date +"%Y-%m-%d")

## Quick Start

Run these skills in order:
1. /strategic-thinking
2. /constitution-builder --product
3. /personas → /jobs-to-be-done → /market-analysis
4. /brand-guidelines → /interaction-design
5. /user-stories → /assumptions-and-risks → /success-metrics

Then transition to DevKit: /specify → /plan → /tasks → /implement
EOF
        print_success "ProdKit workspace ready"
    fi
}

install_claude_md() {
    echo ""
    echo -e "  ${BOLD}Installing CLAUDE.md${NC}"
    echo ""

    if [ ! -f "CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/CLAUDE.md" ./CLAUDE.md
        print_success "Created CLAUDE.md (Claude reads this at session start)"
    else
        print_warning "CLAUDE.md exists, skipping"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

show_completion() {
    local skill_count=$(find .claude/skills -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    local agent_count=$(ls -1 .claude/agents/*.md 2>/dev/null | wc -l | tr -d ' ')

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
    print_success "${skill_count} skills in .claude/skills/"
    print_success "${agent_count} agent personas in .claude/agents/"
    [ "$INSTALL_DEVKIT" = true ] && print_success "DevKit workspace in .devkit/"
    [ "$INSTALL_PRODKIT" = true ] && print_success "ProdKit workspace in .prodkit/"
    print_success "Session hooks in .claude/hooks/"
    print_success "CLAUDE.md (project instructions)"

    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Next Steps${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "  ${CYAN}1.${NC} Start Claude Code in this directory"
    echo ""
    echo -e "  ${CYAN}2.${NC} Begin your workflow:"
    echo ""

    if [ "$INSTALL_PRODKIT" = true ]; then
        echo -e "     ${DIM}Full product development:${NC}"
        echo -e "     ${GREEN}/strategic-thinking${NC} → ${GREEN}/personas${NC} → ${GREEN}/specify${NC} → ${GREEN}/implement${NC}"
        echo ""
    fi

    if [ "$INSTALL_DEVKIT" = true ]; then
        echo -e "     ${DIM}Quick implementation:${NC}"
        echo -e "     ${GREEN}/brainstorming${NC} → ${GREEN}/specify${NC} → ${GREEN}/implement${NC}"
        echo ""
    fi

    echo -e "  ${CYAN}3.${NC} Type ${GREEN}/help${NC} to see all available skills"
    echo ""
    echo ""
    echo -e "  ${DIM}Happy shipping! 🚀${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# NON-INTERACTIVE MODE (CLI flags)
# ═══════════════════════════════════════════════════════════════════════════════

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Interactive installer for ShipKit. Run without arguments for guided setup.

OPTIONS:
    --preset <name>     Skip interactive menu (solo|all|devkit-only|prodkit-only)
    --github <URL>      Clone from GitHub instead of local
    --branch <name>     GitHub branch (default: main)
    --yes, -y           Skip confirmations
    --help              Show this help

EXAMPLES:
    # Interactive mode (recommended)
    bash install.sh

    # Non-interactive with preset
    bash install.sh --preset solo -y

    # From GitHub
    bash install.sh --github https://github.com/user/shipkit.git --preset solo

EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --github) GITHUB_URL="$2"; shift 2;;
            --branch) GITHUB_BRANCH="$2"; shift 2;;
            --preset) PRESET="$2"; INTERACTIVE=false; shift 2;;
            --all) PRESET="all"; INTERACTIVE=false; shift;;
            --devkit-only) PRESET="devkit-only"; INTERACTIVE=false; shift;;
            --prodkit-only) PRESET="prodkit-only"; INTERACTIVE=false; shift;;
            --yes|-y) INTERACTIVE=false; shift;;
            --help) show_usage; exit 0;;
            *) echo "Unknown option: $1"; show_usage; exit 1;;
        esac
    done

    # Default preset if specified non-interactively but no preset given
    [ "$INTERACTIVE" = false ] && [ -z "$PRESET" ] && PRESET="solo"

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

        if git clone --depth 1 --branch "$GITHUB_BRANCH" "$GITHUB_URL" "$TEMP_DIR" 2>/dev/null; then
            print_success "Repository cloned"
            SCRIPT_DIR="$TEMP_DIR"
        else
            print_error "Failed to clone repository"
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

    # Interactive or preset selection
    if [ "$INTERACTIVE" = true ]; then
        # Confirm installation location
        echo ""
        if ! confirm "Install ShipKit to ${CYAN}$PWD${NC}?"; then
            print_info "Installation cancelled."
            exit 0
        fi

        select_preset_interactive
    else
        echo ""
        print_info "Using preset: ${BOLD}$PRESET${NC}"
    fi

    # Perform installation
    install_skills
    install_agents
    install_hooks
    install_infrastructure
    install_claude_md

    # Show completion
    show_completion
}

# Run main
main "$@"
