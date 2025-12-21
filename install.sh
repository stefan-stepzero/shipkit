#!/usr/bin/env bash
# install.sh - Shipkit Installer (Radically Simple Edition)
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
TARGET_DIR=""
CONSTITUTION_TEMPLATE=""
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
    echo -e "${DIM}         Complete Product Development Framework${NC}"
    echo -e "${DIM}              Discovery → Specification → Code${NC}"
    echo ""
}

show_mini_logo() {
    echo ""
    echo -e "${BRIGHT_MAGENTA}  ╭──────────────────────────────────────╮${NC}"
    echo -e "${BRIGHT_MAGENTA}  │${NC}  ${BOLD}ShipKit${NC} ${DIM}• Radically Simple${NC}         ${BRIGHT_MAGENTA}│${NC}"
    echo -e "${BRIGHT_MAGENTA}  ╰──────────────────────────────────────╯${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE MENU FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

select_option() {
    local prompt="$1"
    shift
    local options=("$@")
    local selected=0
    local key=""

    tput civis 2>/dev/null || true

    while true; do
        echo -e "\n  ${BOLD}${prompt}${NC}\n"

        for i in "${!options[@]}"; do
            if [ $i -eq $selected ]; then
                echo -e "  ${BRIGHT_CYAN}❯${NC} ${BRIGHT_WHITE}${options[$i]}${NC}"
            else
                echo -e "    ${DIM}${options[$i]}${NC}"
            fi
        done

        echo -e "\n  ${DIM}↑/↓ to move, Enter to select${NC}"

        read -rsn1 key

        if [[ $key == $'\x1b' ]]; then
            read -rsn2 key
            case $key in
                '[A')
                    ((selected--))
                    [ $selected -lt 0 ] && selected=$((${#options[@]} - 1))
                    ;;
                '[B')
                    ((selected++))
                    [ $selected -ge ${#options[@]} ] && selected=0
                    ;;
            esac
        elif [[ $key == "" ]]; then
            break
        fi

        local lines=$((${#options[@]} + 4))
        tput cuu $lines 2>/dev/null || printf "\033[${lines}A"
        tput el 2>/dev/null || true
    done

    tput cnorm 2>/dev/null || true

    SELECTED_INDEX=$selected
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

    local dirs=("install/skills" "install/agents" "install/constitutions" "install/workspace" "install/hooks")

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
        echo -e "  ${DIM}Expected shipkit structure at: $SCRIPT_DIR${NC}"
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
# CONSTITUTION TEMPLATE SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

select_constitution_template() {
    echo -e "\n  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Choose your constitution template${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    select_option "What type of project is this?" \
        "🏢 B2C SaaS - Fundable consumer product (Recommended)" \
        "🏛️  B2B SaaS - Enterprise-ready, compliant" \
        "⚡ Side Project - Ship in 1 week, minimal rules" \
        "🔬 Experimental - Learn and break things"

    case $SELECTED_INDEX in
        0) CONSTITUTION_TEMPLATE="b2c-saas" ;;
        1) CONSTITUTION_TEMPLATE="b2b-saas" ;;
        2) CONSTITUTION_TEMPLATE="side-project" ;;
        3) CONSTITUTION_TEMPLATE="experimental" ;;
    esac

    echo ""
    print_success "Selected: ${BOLD}$CONSTITUTION_TEMPLATE${NC}"
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

    print_loading "Installing all skills"
    cp -r "$SCRIPT_DIR/install/skills/"* .claude/skills/

    local skill_count=$(ls -1d .claude/skills/*/ 2>/dev/null | wc -l | tr -d ' ')
    print_success "Installed $skill_count skills"
    print_bullet "Product discovery, technical specs, development workflow"
}

install_agents() {
    echo ""
    echo -e "  ${BOLD}Installing agent personas${NC}"
    echo ""

    mkdir -p .claude/agents

    local count=0
    for agent in "$SCRIPT_DIR/install/agents"/*.md; do
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

install_constitution() {
    echo ""
    echo -e "  ${BOLD}Installing constitution template${NC}"
    echo ""

    mkdir -p .claude/constitutions

    # Copy core.md
    if [ -f "$SCRIPT_DIR/install/constitutions/$CONSTITUTION_TEMPLATE/core.md" ]; then
        cp "$SCRIPT_DIR/install/constitutions/$CONSTITUTION_TEMPLATE/core.md" .claude/constitutions/core.md
        print_success "Installed core constitution"
    fi

    # Copy product/ directory if exists
    if [ -d "$SCRIPT_DIR/install/constitutions/$CONSTITUTION_TEMPLATE/product" ]; then
        cp -r "$SCRIPT_DIR/install/constitutions/$CONSTITUTION_TEMPLATE/product" .claude/constitutions/
        local product_count=$(find .claude/constitutions/product -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$product_count" -gt 0 ]; then
            print_success "Installed $product_count product constitutions"
        fi
    fi

    # Copy technical/ directory if exists
    if [ -d "$SCRIPT_DIR/install/constitutions/$CONSTITUTION_TEMPLATE/technical" ]; then
        cp -r "$SCRIPT_DIR/install/constitutions/$CONSTITUTION_TEMPLATE/technical" .claude/constitutions/
        local technical_count=$(find .claude/constitutions/technical -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$technical_count" -gt 0 ]; then
            print_success "Installed $technical_count technical constitutions"
        fi
    fi

    print_bullet "Template: ${CYAN}$CONSTITUTION_TEMPLATE${NC}"
}

install_hooks() {
    echo ""
    echo -e "  ${BOLD}Installing session hooks${NC}"
    echo ""

    mkdir -p .claude/hooks

    # Copy hook scripts (excluding settings.json)
    for file in "$SCRIPT_DIR/install/hooks/"*; do
        filename=$(basename "$file")
        if [ "$filename" != "settings.json" ]; then
            cp "$file" .claude/hooks/
        fi
    done
    chmod +x .claude/hooks/*.sh 2>/dev/null || true

    # Configure settings.json
    SETTINGS_FILE=".claude/settings.json"
    if [ ! -f "$SETTINGS_FILE" ]; then
        if [ -f "$SCRIPT_DIR/install/hooks/settings.json" ]; then
            cp "$SCRIPT_DIR/install/hooks/settings.json" "$SETTINGS_FILE"
            print_success "Installed settings.json with permissions & hooks"
        else
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
            print_success "Created basic settings.json with hooks"
        fi
    else
        print_warning "settings.json exists, preserving your custom config"
    fi
}

install_workspace() {
    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Setting up workspace${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    print_loading "Creating .shipkit/ workspace"

    # Create unified workspace structure
    mkdir -p .shipkit/{specs,discovery,strategy,requirements,brand,design,metrics,scripts,templates}

    # Copy scripts
    cp -r "$SCRIPT_DIR/install/workspace/scripts/bash" .shipkit/scripts/
    cp -r "$SCRIPT_DIR/install/workspace/scripts/powershell" .shipkit/scripts/ 2>/dev/null || true
    chmod +x .shipkit/scripts/bash/*.sh 2>/dev/null || true

    # Copy templates
    cp -r "$SCRIPT_DIR/install/workspace/templates/"* .shipkit/templates/ 2>/dev/null || true

    # Create README
    cat > .shipkit/README.md <<EOF
# Shipkit Workspace

Generated: $(date +"%Y-%m-%d")
Constitution: $CONSTITUTION_TEMPLATE

## Unified Workspace Structure

This workspace contains all your product and development artifacts:

### Product Discovery
- \`strategy/\` - Business strategy, value propositions
- \`discovery/\` - Personas, JTBD, market analysis
- \`brand/\` - Brand guidelines, visual direction
- \`design/\` - Interaction design, user journeys
- \`requirements/\` - User stories, acceptance criteria
- \`metrics/\` - Success metrics, KPIs

### Technical Development
- \`specs/\` - Feature specifications
- \`scripts/\` - Automation scripts
- \`templates/\` - Document templates

## Recommended Workflow

### Full Product Development
1. \`/strategic-thinking\` - Define your strategy
2. \`/personas\` → \`/jobs-to-be-done\` → \`/market-analysis\`
3. \`/brand-guidelines\` → \`/interaction-design\`
4. \`/user-stories\` → \`/assumptions-and-risks\` → \`/success-metrics\`
5. \`/specify\` → \`/plan\` → \`/tasks\` → \`/implement\`

### Quick Implementation
1. \`/brainstorming\` - Generate ideas
2. \`/specify\` - Write specification
3. \`/plan\` → \`/tasks\` → \`/implement\`

Type \`/help\` to see all available skills.
EOF

    print_success "Shipkit workspace ready"
    print_bullet "Unified structure for product & development"
}

install_claude_md() {
    echo ""
    echo -e "  ${BOLD}Installing CLAUDE.md${NC}"
    echo ""

    if [ ! -f "CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/install/CLAUDE.md" ./CLAUDE.md
        print_success "Created CLAUDE.md (Claude reads this at session start)"
    else
        print_warning "CLAUDE.md exists, skipping"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETION SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

show_completion() {
    local skill_count=$(ls -1d .claude/skills/*/ 2>/dev/null | wc -l | tr -d ' ')
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
    print_success "Unified workspace in .shipkit/"
    print_success "Session hooks in .claude/hooks/"
    print_success "Constitution template: ${CONSTITUTION_TEMPLATE}"
    print_success "CLAUDE.md (project instructions)"

    echo ""
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${BOLD}Next Steps${NC}"
    echo -e "  ${BRIGHT_MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "  ${CYAN}1.${NC} Start Claude Code in ${CYAN}$TARGET_DIR${NC}"
    echo ""
    echo -e "  ${CYAN}2.${NC} Begin your workflow:"
    echo ""
    echo -e "     ${DIM}Full product development:${NC}"
    echo -e "     ${GREEN}/strategic-thinking${NC} → ${GREEN}/personas${NC} → ${GREEN}/specify${NC} → ${GREEN}/implement${NC}"
    echo ""
    echo -e "     ${DIM}Quick implementation:${NC}"
    echo -e "     ${GREEN}/brainstorming${NC} → ${GREEN}/specify${NC} → ${GREEN}/implement${NC}"
    echo ""
    echo -e "  ${CYAN}3.${NC} Type ${GREEN}/help${NC} to see all available skills"
    echo ""
    echo ""
    echo -e "  ${DIM}Happy shipping! 🚀${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# USAGE & CLI
# ═══════════════════════════════════════════════════════════════════════════════

show_usage() {
    cat << EOF
Usage: $0 [TARGET_DIR] [OPTIONS]

Radically simple installer for Shipkit. Run without arguments for guided setup in current directory.

ARGUMENTS:
    TARGET_DIR                 Target directory to install shipkit (optional, defaults to current directory)

OPTIONS:
    --target <path>            Target directory (alternative to positional argument)
    --constitution <template>  Choose constitution template (b2c-saas|b2b-saas|side-project|experimental)
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

    # Non-interactive with B2B SaaS constitution
    bash install.sh /path/to/project --constitution b2b-saas -y

    # From GitHub to specific directory
    bash install.sh --target ~/my-project --github https://github.com/user/shipkit.git --constitution side-project

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
            --constitution) CONSTITUTION_TEMPLATE="$2"; shift 2;;
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

    # Default to current directory if no target specified
    if [ -z "$TARGET_DIR" ]; then
        TARGET_DIR="$PWD"
    fi

    # Convert to absolute path
    if [[ "$TARGET_DIR" != /* ]]; then
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

    # Confirm installation location
    if [ "$INTERACTIVE" = true ]; then
        echo ""
        if ! confirm "Install ShipKit to ${CYAN}$TARGET_DIR${NC}?"; then
            print_info "Installation cancelled."
            exit 0
        fi

        # Select constitution template
        select_constitution_template
    else
        # Non-interactive: default constitution template
        [ -z "$CONSTITUTION_TEMPLATE" ] && CONSTITUTION_TEMPLATE="b2c-saas"
        echo ""
        print_info "Using constitution template: ${BOLD}$CONSTITUTION_TEMPLATE${NC}"
    fi

    # Perform installation
    print_info "Installing shipkit (all skills + unified workspace)..."
    install_skills
    install_agents
    install_constitution
    install_hooks
    install_workspace
    install_claude_md

    # Show completion
    show_completion
}

# Run main
main "$@"
