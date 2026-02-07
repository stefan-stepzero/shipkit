#!/usr/bin/env node
/**
 * Shipkit Mission Control Server
 *
 * Central server for monitoring multiple Claude Code instances.
 * - Receives events from reporter hooks
 * - Serves dashboard UI
 * - Queues commands for instances
 *
 * Port: 7777 (quad 7)
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.MISSION_CONTROL_PORT || 7777;
const SERVER_VERSION = '1.1.0';

// Hub paths - server runs from ~/.shipkit-mission-control/server/
const HUB_ROOT = path.join(__dirname, '..');
const DATA_DIR = path.join(HUB_ROOT, '.shipkit', 'mission-control');
const INBOX_DIR = path.join(DATA_DIR, 'inbox');
const CODEBASES_DIR = path.join(DATA_DIR, 'codebases');
const EVENTS_FILE = path.join(DATA_DIR, 'events.jsonl');
const DASHBOARD_DIR = path.join(HUB_ROOT, 'dashboard', 'dist');
const DASHBOARD_INDEX = path.join(DASHBOARD_DIR, 'index.html');

// MIME types for static file serving
const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
};

// In-memory storage
const instances = new Map(); // sessionId -> instance data
const events = []; // Recent events (capped at 1000)
const codebases = new Map(); // projectPath -> codebase analytics
const MAX_EVENTS = 1000;
const INSTANCE_TIMEOUT = 5 * 60 * 1000; // 5 minutes
const STALE_REMOVE_TIMEOUT = 60 * 60 * 1000; // 1 hour

// Skill relationship knowledge for recommendations
const SKILL_KNOWLEDGE = {
    // Skill dependencies and staleness thresholds
    "shipkit-spec": {
        suggests: ["shipkit-plan", "shipkit-architecture-memory"],
        staleAfterDays: 14,
        category: "planning"
    },
    "shipkit-plan": {
        suggests: ["shipkit-build-relentlessly", "shipkit-implement-independently"],
        staleAfterDays: 7,
        category: "planning"
    },
    "shipkit-project-context": {
        suggests: ["shipkit-codebase-index", "shipkit-project-status"],
        staleAfterDays: 30,
        category: "discovery"
    },
    "shipkit-project-status": {
        suggests: ["shipkit-spec", "shipkit-plan"],
        staleAfterDays: 7,
        category: "discovery"
    },
    "shipkit-architecture-memory": {
        staleAfterDays: 14,
        category: "knowledge"
    },
    "shipkit-work-memory": {
        staleAfterDays: 1,
        category: "knowledge"
    },
    "shipkit-data-contracts": {
        staleAfterDays: 14,
        category: "knowledge"
    },
    "shipkit-build-relentlessly": {
        suggests: ["shipkit-test-relentlessly", "shipkit-verify"],
        category: "execution"
    },
    "shipkit-test-relentlessly": {
        suggests: ["shipkit-verify", "shipkit-preflight"],
        category: "execution"
    },
    "shipkit-verify": {
        suggests: ["shipkit-preflight"],
        staleAfterDays: 3,
        category: "quality"
    },
    "shipkit-preflight": {
        staleAfterDays: 7,
        category: "quality"
    },
    "shipkit-goals": {
        suggests: ["shipkit-spec", "shipkit-plan"],
        staleAfterDays: 14,
        category: "planning"
    },
    "shipkit-why-project": {
        suggests: ["shipkit-goals", "shipkit-product-discovery"],
        staleAfterDays: 30,
        category: "discovery"
    },
    "shipkit-product-discovery": {
        suggests: ["shipkit-spec", "shipkit-ux-audit"],
        staleAfterDays: 30,
        category: "discovery"
    },
    "shipkit-feedback-bug": {
        suggests: ["shipkit-plan", "shipkit-test-cases"],
        staleAfterDays: 7,
        category: "quality"
    },
    "shipkit-prompt-audit": {
        suggests: ["shipkit-verify"],
        staleAfterDays: 14,
        category: "quality"
    },
    "shipkit-scale-ready": {
        suggests: ["shipkit-preflight"],
        staleAfterDays: 14,
        category: "quality"
    },
    "shipkit-ux-audit": {
        suggests: ["shipkit-spec"],
        staleAfterDays: 14,
        category: "quality"
    },
    "shipkit-user-instructions": {
        staleAfterDays: 3,
        category: "knowledge"
    },
    "shipkit-test-cases": {
        suggests: ["shipkit-test-relentlessly"],
        staleAfterDays: 7,
        category: "quality"
    },
    "shipkit-codebase-index": {
        suggests: ["shipkit-project-context"],
        staleAfterDays: 7,
        category: "discovery"
    },
    "shipkit-lint-relentlessly": {
        suggests: ["shipkit-verify"],
        category: "execution"
    },
    "shipkit-implement-independently": {
        suggests: ["shipkit-verify", "shipkit-test-relentlessly"],
        category: "execution"
    }
};

// Ensure data directories exist
[INBOX_DIR, CODEBASES_DIR, DATA_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Load persisted data on startup
function loadPersistedData() {
    // Load codebases
    try {
        const files = fs.readdirSync(CODEBASES_DIR);
        for (const file of files) {
            if (file.endsWith('.json')) {
                const data = JSON.parse(fs.readFileSync(path.join(CODEBASES_DIR, file), 'utf-8'));
                codebases.set(data.projectPath, data);
            }
        }
        console.log(`Loaded ${codebases.size} codebases from disk`);
    } catch (e) {
        // No persisted data yet
    }

    // Load recent events
    try {
        if (fs.existsSync(EVENTS_FILE)) {
            const lines = fs.readFileSync(EVENTS_FILE, 'utf-8').trim().split('\n');
            const recentLines = lines.slice(-MAX_EVENTS);
            for (const line of recentLines) {
                if (line) events.push(JSON.parse(line));
            }
            console.log(`Loaded ${events.length} events from disk`);
        }
    } catch (e) {
        // No events yet
    }
}

// Save codebase to disk
function persistCodebase(codebase) {
    const safeName = codebase.projectName.replace(/[^a-zA-Z0-9-_]/g, '_');
    const filePath = path.join(CODEBASES_DIR, `${safeName}.json`);
    fs.writeFileSync(filePath, JSON.stringify(codebase, null, 2));
}

// Append event to disk
function persistEvent(eventData) {
    fs.appendFileSync(EVENTS_FILE, JSON.stringify(eventData) + '\n');
}

// Load data on startup
loadPersistedData();

/**
 * Update or register an instance
 */
function updateInstance(eventData) {
    const { sessionId, project, projectPath, event, tool, skill, timestamp } = eventData;

    const existing = instances.get(sessionId) || {
        sessionId,
        project,
        projectPath,
        firstSeen: timestamp,
        toolCount: 0,
        skills: []
    };

    existing.lastSeen = timestamp;
    existing.lastEvent = event;
    existing.lastTool = tool;
    existing.toolCount++;

    if (skill && !existing.skills.includes(skill)) {
        existing.skills.push(skill);
    }

    // Determine status
    if (event === 'Stop') {
        existing.status = 'stopped';
        existing.mode = null;
    } else if (event === 'SessionStart') {
        existing.status = 'active';
        existing.toolCount = 0;
        existing.mode = null;
    } else {
        existing.status = 'active';
    }

    // Track mode from reporter (e.g. "standby")
    if (eventData.mode) {
        existing.mode = eventData.mode;
    }

    instances.set(sessionId, existing);

    // Update codebase analytics
    if (projectPath) {
        updateCodebaseAnalytics(projectPath, project, skill, timestamp);
    }

    // Store artifacts if present (JSON files from .shipkit/)
    if (eventData.artifacts && projectPath) {
        updateCodebaseArtifacts(projectPath, eventData.artifacts);
    }
}

/**
 * Update codebase-level skill analytics
 */
function updateCodebaseAnalytics(projectPath, projectName, skill, timestamp) {
    let codebase = codebases.get(projectPath);

    if (!codebase) {
        codebase = {
            projectPath,
            projectName,
            firstSeen: timestamp,
            lastActivity: timestamp,
            skills: {},
            totalSkillUses: 0
        };
        codebases.set(projectPath, codebase);
    }

    codebase.lastActivity = timestamp;
    codebase.projectName = projectName; // Update in case it changed

    // Track skill usage
    if (skill) {
        if (!codebase.skills[skill]) {
            codebase.skills[skill] = {
                name: skill,
                firstUsed: timestamp,
                lastUsed: timestamp,
                useCount: 0
            };
        }

        codebase.skills[skill].lastUsed = timestamp;
        codebase.skills[skill].useCount++;
        codebase.totalSkillUses++;
    }

    // Persist to disk
    persistCodebase(codebase);
}

/**
 * Store JSON artifacts from .shipkit/ for dashboard rendering
 */
function updateCodebaseArtifacts(projectPath, artifacts) {
    let codebase = codebases.get(projectPath);
    if (!codebase) return;

    if (!codebase.artifacts) {
        codebase.artifacts = {};
    }

    // Merge new artifacts (keyed by filename, e.g. "goals.json")
    for (const [filename, data] of Object.entries(artifacts)) {
        // Lightweight validation - warn on missing required fields
        const warnings = [];
        if (!data.type) warnings.push('missing type');
        if (!data.version) warnings.push('missing version');
        if (!data.summary) warnings.push('missing summary');

        codebase.artifacts[filename] = {
            ...data,
            _receivedAt: Date.now(),
            ...(warnings.length > 0 && { _validationWarnings: warnings })
        };

        if (warnings.length > 0) {
            console.warn(`Artifact ${filename}: ${warnings.join(', ')}`);
        }
    }

    persistCodebase(codebase);
}

/**
 * Generate recommendations for a codebase
 * Merges hardcoded rules with Claude-generated analysis (Claude takes priority)
 */
function generateRecommendations(codebase) {
    // If we have fresh Claude analysis (less than 1 hour old), use it
    if (codebase.claudeRecommendations) {
        const analyzed = new Date(codebase.claudeRecommendations.analyzedAt);
        const hourAgo = new Date(Date.now() - 60 * 60 * 1000);

        if (analyzed > hourAgo) {
            return codebase.claudeRecommendations.recommendations.slice(0, 5);
        }
    }

    // Fall back to hardcoded rules
    const recommendations = [];
    const now = Date.now() / 1000;
    const DAY_SECONDS = 86400;

    // Check for stale skills
    for (const [skillName, skillData] of Object.entries(codebase.skills)) {
        const knowledge = SKILL_KNOWLEDGE[skillName];
        if (!knowledge) continue;

        const daysSinceUse = (now - skillData.lastUsed) / DAY_SECONDS;

        // Check staleness
        if (knowledge.staleAfterDays && daysSinceUse > knowledge.staleAfterDays) {
            recommendations.push({
                type: 'stale',
                skill: skillName,
                message: `${skillName} last used ${Math.floor(daysSinceUse)} days ago - consider refreshing`,
                priority: knowledge.category === 'knowledge' ? 'high' : 'medium',
                action: `/${skillName}`,
                source: 'hardcoded'
            });
        }

        // Check for suggested follow-ups not yet used
        if (knowledge.suggests) {
            for (const suggestedSkill of knowledge.suggests) {
                if (!codebase.skills[suggestedSkill]) {
                    recommendations.push({
                        type: 'suggested',
                        skill: suggestedSkill,
                        message: `After ${skillName}, consider running ${suggestedSkill}`,
                        priority: 'low',
                        action: `/${suggestedSkill}`,
                        source: 'hardcoded'
                    });
                }
            }
        }
    }

    // Check for missing foundational skills
    const foundational = ['shipkit-project-context', 'shipkit-project-status'];
    for (const skill of foundational) {
        if (!codebase.skills[skill]) {
            recommendations.push({
                type: 'missing',
                skill: skill,
                message: `${skill} has never been run - recommended for new projects`,
                priority: 'high',
                action: `/${skill}`,
                source: 'hardcoded'
            });
        }
    }

    // Sort by priority
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    recommendations.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

    return recommendations.slice(0, 5); // Top 5 recommendations
}

/**
 * Get quick action skills based on context
 */
function getQuickActions(codebase) {
    const actions = [];
    const usedSkills = Object.keys(codebase?.skills || {});

    // Always useful
    actions.push(
        { skill: 'shipkit-project-status', label: 'Check Status', icon: '📊' },
        { skill: 'shipkit-work-memory', label: 'Log Progress', icon: '📝' }
    );

    // Context-aware actions
    if (usedSkills.includes('shipkit-spec') && !usedSkills.includes('shipkit-plan')) {
        actions.push({ skill: 'shipkit-plan', label: 'Create Plan', icon: '📋' });
    }

    if (usedSkills.includes('shipkit-plan')) {
        actions.push(
            { skill: 'shipkit-build-relentlessly', label: 'Build', icon: '🔨' },
            { skill: 'shipkit-test-relentlessly', label: 'Test', icon: '🧪' }
        );
    }

    // Quality checks
    actions.push(
        { skill: 'shipkit-verify', label: 'Verify', icon: '✅' },
        { skill: 'shipkit-preflight', label: 'Preflight', icon: '🚀' }
    );

    return actions.slice(0, 8); // Max 8 quick actions
}

/**
 * Add event to log
 */
function addEvent(eventData) {
    const enrichedEvent = {
        ...eventData,
        receivedAt: Date.now()
    };

    events.unshift(enrichedEvent);

    // Cap events in memory
    if (events.length > MAX_EVENTS) {
        events.pop();
    }

    // Persist to disk
    persistEvent(enrichedEvent);
}

/**
 * Clean up stale instances
 */
function cleanupInstances() {
    const now = Date.now();
    for (const [sessionId, instance] of instances) {
        const lastSeenMs = instance.lastSeen * 1000;
        if (now - lastSeenMs > STALE_REMOVE_TIMEOUT) {
            instances.delete(sessionId);
        } else if (now - lastSeenMs > INSTANCE_TIMEOUT) {
            instance.status = 'stale';
        }
    }
}

// Run cleanup every minute
setInterval(cleanupInstances, 60000);

/**
 * Clean up processed command files older than 1 hour
 */
const PROCESSED_MAX_AGE = 60 * 60 * 1000; // 1 hour

function cleanupProcessedCommands() {
    try {
        if (!fs.existsSync(INBOX_DIR)) return;

        const sessionDirs = fs.readdirSync(INBOX_DIR, { withFileTypes: true });
        for (const entry of sessionDirs) {
            if (!entry.isDirectory()) continue;

            const sessionDir = path.join(INBOX_DIR, entry.name);
            const files = fs.readdirSync(sessionDir);

            for (const file of files) {
                if (!file.endsWith('.processed')) continue;

                const filePath = path.join(sessionDir, file);
                try {
                    const stat = fs.statSync(filePath);
                    if (Date.now() - stat.mtimeMs > PROCESSED_MAX_AGE) {
                        fs.unlinkSync(filePath);
                    }
                } catch (e) {
                    // Best effort cleanup
                }
            }

            // Remove empty session directories
            try {
                const remaining = fs.readdirSync(sessionDir);
                if (remaining.length === 0) {
                    fs.rmdirSync(sessionDir);
                }
            } catch (e) {
                // Best effort
            }
        }
    } catch (e) {
        // Best effort cleanup
    }
}

// Run processed cleanup every 10 minutes
setInterval(cleanupProcessedCommands, 10 * 60 * 1000);

/**
 * Parse JSON body from request
 */
function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        let size = 0;
        const MAX_BODY = 1024 * 1024; // 1MB
        req.on('data', chunk => {
            size += chunk.length;
            if (size > MAX_BODY) {
                reject(new Error('Body too large'));
                req.destroy();
                return;
            }
            body += chunk;
        });
        req.on('end', () => {
            try {
                resolve(body ? JSON.parse(body) : {});
            } catch (e) {
                reject(e);
            }
        });
        req.on('error', reject);
    });
}

/**
 * Send JSON response
 */
function sendJson(res, data, status = 200) {
    res.writeHead(status, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    });
    res.end(JSON.stringify(data));
}

/**
 * Send HTML response
 */
function sendHtml(res, html) {
    res.writeHead(200, {
        'Content-Type': 'text/html',
        'Access-Control-Allow-Origin': '*'
    });
    res.end(html);
}

/**
 * Main request handler
 */
async function handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    // CORS preflight
    if (req.method === 'OPTIONS') {
        res.writeHead(200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        });
        res.end();
        return;
    }

    try {
        // Health check
        if (pathname === '/health') {
            sendJson(res, { status: 'ok', version: SERVER_VERSION, uptime: process.uptime() });
            return;
        }

        // Static files from Vite build (CSS, JS, assets)
        if (pathname.startsWith('/assets/') || pathname === '/vite.svg') {
            const filePath = path.resolve(DASHBOARD_DIR, '.' + pathname);
            if (!filePath.startsWith(path.resolve(DASHBOARD_DIR))) {
                sendJson(res, { error: 'Forbidden' }, 403);
                return;
            }
            if (fs.existsSync(filePath)) {
                const ext = path.extname(filePath);
                const mime = MIME_TYPES[ext] || 'application/octet-stream';
                res.writeHead(200, {
                    'Content-Type': mime,
                    'Access-Control-Allow-Origin': '*',
                    'Cache-Control': pathname.startsWith('/assets/') ? 'public, max-age=31536000, immutable' : 'no-cache',
                });
                fs.createReadStream(filePath).pipe(res);
                return;
            }
        }

        // Dashboard root
        if (pathname === '/' || pathname === '/dashboard') {
            if (fs.existsSync(DASHBOARD_INDEX)) {
                const html = fs.readFileSync(DASHBOARD_INDEX, 'utf-8');
                sendHtml(res, html);
            } else {
                sendHtml(res, getEmbeddedDashboard());
            }
            return;
        }

        // API: List instances
        if (pathname === '/api/instances' && req.method === 'GET') {
            cleanupInstances();
            const instanceList = Array.from(instances.values())
                .sort((a, b) => b.lastSeen - a.lastSeen);
            sendJson(res, { instances: instanceList });
            return;
        }

        // API: Get events
        if (pathname === '/api/events' && req.method === 'GET') {
            const limit = parseInt(parsedUrl.query.limit) || 100;
            const sessionId = parsedUrl.query.sessionId;

            let filtered = events;
            if (sessionId) {
                filtered = events.filter(e => e.sessionId === sessionId);
            }

            sendJson(res, { events: filtered.slice(0, limit) });
            return;
        }

        // API: Receive event from hook
        if (pathname === '/api/events' && req.method === 'POST') {
            const eventData = await parseBody(req);
            updateInstance(eventData);
            addEvent(eventData);
            sendJson(res, { received: true });
            return;
        }

        // API: Send command to instance
        if (pathname === '/api/command' && req.method === 'POST') {
            const { sessionId, prompt, source } = await parseBody(req);

            if (!sessionId || !prompt) {
                sendJson(res, { error: 'sessionId and prompt required' }, 400);
                return;
            }

            // Write command to queue directory: inbox/{sessionId}/{timestamp}.json
            const sessionDir = path.join(INBOX_DIR, sessionId);
            if (!fs.existsSync(sessionDir)) {
                fs.mkdirSync(sessionDir, { recursive: true });
            }

            const timestamp = Date.now();
            const commandFile = path.join(sessionDir, `${timestamp}.json`);
            const command = {
                prompt,
                source: source || 'Mission Control Dashboard',
                timestamp
            };

            fs.writeFileSync(commandFile, JSON.stringify(command, null, 2));
            sendJson(res, { queued: true, sessionId, commandId: String(timestamp) });
            return;
        }

        // API: Get command queue for a session
        if (pathname.startsWith('/api/queue/') && req.method === 'GET') {
            const sessionId = decodeURIComponent(pathname.replace('/api/queue/', ''));
            const sessionDir = path.join(INBOX_DIR, sessionId);

            const queue = { pending: [], inflight: [], processed: [] };

            if (fs.existsSync(sessionDir) && fs.statSync(sessionDir).isDirectory()) {
                try {
                    const files = fs.readdirSync(sessionDir).sort();
                    for (const file of files) {
                        const filePath = path.join(sessionDir, file);
                        let status, commandId;

                        if (file.endsWith('.json')) {
                            status = 'pending';
                            commandId = file.replace('.json', '');
                        } else if (file.endsWith('.inflight')) {
                            status = 'inflight';
                            commandId = file.replace('.inflight', '');
                        } else if (file.endsWith('.processed')) {
                            status = 'processed';
                            commandId = file.replace('.processed', '');
                        } else {
                            continue;
                        }

                        // Read command content
                        let prompt = '', source = '';
                        try {
                            const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
                            prompt = data.prompt || '';
                            source = data.source || '';
                        } catch (e) {
                            // File might be empty or corrupt
                        }

                        const item = {
                            commandId,
                            status,
                            prompt: prompt.substring(0, 200),
                            source,
                            timestamp: parseInt(commandId) || 0
                        };

                        queue[status].push(item);
                    }
                } catch (e) {
                    // Best effort
                }
            }

            sendJson(res, {
                sessionId,
                ...queue,
                total: queue.pending.length + queue.inflight.length + queue.processed.length
            });
            return;
        }

        // API: Get stats
        if (pathname === '/api/stats' && req.method === 'GET') {
            cleanupInstances();
            const activeCount = Array.from(instances.values())
                .filter(i => i.status === 'active').length;

            sendJson(res, {
                totalInstances: instances.size,
                activeInstances: activeCount,
                totalCodebases: codebases.size,
                totalEvents: events.length,
                uptime: process.uptime()
            });
            return;
        }

        // API: Get codebase analytics
        if (pathname === '/api/codebases' && req.method === 'GET') {
            const codebaseList = Array.from(codebases.values()).map(cb => ({
                ...cb,
                recommendations: generateRecommendations(cb),
                quickActions: getQuickActions(cb),
                skillCount: Object.keys(cb.skills).length
            }));

            sendJson(res, { codebases: codebaseList });
            return;
        }

        // API: Get specific codebase
        if (pathname.startsWith('/api/codebases/') && req.method === 'GET') {
            const projectPath = decodeURIComponent(pathname.replace('/api/codebases/', ''));
            const codebase = codebases.get(projectPath);

            if (!codebase) {
                sendJson(res, { error: 'Codebase not found' }, 404);
                return;
            }

            sendJson(res, {
                ...codebase,
                recommendations: generateRecommendations(codebase),
                quickActions: getQuickActions(codebase)
            });
            return;
        }

        // API: Get quick actions for an instance
        if (pathname === '/api/quick-actions' && req.method === 'GET') {
            const sessionId = parsedUrl.query.sessionId;
            const instance = instances.get(sessionId);

            if (!instance) {
                // Return default actions
                sendJson(res, { actions: getQuickActions(null) });
                return;
            }

            const codebase = codebases.get(instance.projectPath);
            sendJson(res, { actions: getQuickActions(codebase) });
            return;
        }

        // API: Update recommendations (from Claude analysis)
        if (pathname === '/api/recommendations' && req.method === 'POST') {
            const { projectPath, recommendations, source, analyzedAt } = await parseBody(req);

            if (!projectPath) {
                sendJson(res, { error: 'projectPath required' }, 400);
                return;
            }

            let codebase = codebases.get(projectPath);
            if (!codebase) {
                // Create codebase entry if it doesn't exist
                codebase = {
                    projectPath,
                    projectName: path.basename(projectPath),
                    firstSeen: Date.now() / 1000,
                    lastActivity: Date.now() / 1000,
                    skills: {},
                    totalSkillUses: 0
                };
                codebases.set(projectPath, codebase);
            }

            // Store Claude-generated recommendations
            codebase.claudeRecommendations = {
                recommendations: recommendations || [],
                source: source || 'claude-analysis',
                analyzedAt: analyzedAt || new Date().toISOString()
            };

            persistCodebase(codebase);

            sendJson(res, { updated: true, projectPath });
            return;
        }

        // SPA fallback - serve React app for unknown routes (client-side routing)
        if (!pathname.startsWith('/api') && fs.existsSync(DASHBOARD_INDEX)) {
            const html = fs.readFileSync(DASHBOARD_INDEX, 'utf-8');
            sendHtml(res, html);
            return;
        }

        // 404
        sendJson(res, { error: 'Not found' }, 404);

    } catch (error) {
        console.error('Request error:', error);
        sendJson(res, { error: error.message }, 500);
    }
}

/**
 * Embedded dashboard (fallback if HTML file not found)
 */
function getEmbeddedDashboard() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mission Control - Claude Code Monitor</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 20px; border-bottom: 1px solid #333; }
        .header h1 { font-size: 24px; display: flex; align-items: center; gap: 10px; }
        .header h1::before { content: '📡'; }
        .stats { display: flex; gap: 20px; margin-top: 10px; }
        .stat { background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 8px; }
        .stat-value { font-size: 24px; font-weight: bold; color: #4ade80; }
        .stat-label { font-size: 12px; color: #888; }
        .container { padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #333; }
        .panel h2 { font-size: 16px; margin-bottom: 15px; color: #888; }
        .instance-card { background: #0f0f1a; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #4ade80; }
        .instance-card.stale { border-left-color: #888; opacity: 0.6; }
        .instance-card.stopped { border-left-color: #f87171; }
        .instance-name { font-weight: bold; font-size: 16px; }
        .instance-path { font-size: 12px; color: #666; margin-top: 4px; font-family: monospace; }
        .instance-meta { display: flex; gap: 15px; margin-top: 10px; font-size: 12px; color: #888; }
        .instance-actions { margin-top: 10px; }
        .btn { background: #3b82f6; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }
        .btn:hover { background: #2563eb; }
        .event-list { max-height: 400px; overflow-y: auto; }
        .event { padding: 8px; border-bottom: 1px solid #222; font-size: 13px; }
        .event-time { color: #666; font-size: 11px; }
        .event-tool { color: #4ade80; }
        .modal { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); align-items: center; justify-content: center; }
        .modal.active { display: flex; }
        .modal-content { background: #1a1a2e; padding: 20px; border-radius: 12px; width: 500px; max-width: 90%; }
        .modal-content h3 { margin-bottom: 15px; }
        .modal-content textarea { width: 100%; height: 120px; background: #0f0f1a; border: 1px solid #333; color: #e0e0e0; padding: 10px; border-radius: 4px; font-family: inherit; resize: vertical; }
        .modal-actions { display: flex; gap: 10px; margin-top: 15px; justify-content: flex-end; }
        .btn-cancel { background: #333; }
        .empty { text-align: center; padding: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Mission Control</h1>
        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="active-count">0</div>
                <div class="stat-label">Active Instances</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="event-count">0</div>
                <div class="stat-label">Events</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="uptime">0s</div>
                <div class="stat-label">Uptime</div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="panel">
            <h2>Instances</h2>
            <div id="instances"><div class="empty">No instances connected yet</div></div>
        </div>
        <div class="panel">
            <h2>Recent Events</h2>
            <div class="event-list" id="events"><div class="empty">No events yet</div></div>
        </div>
    </div>

    <div class="modal" id="inject-modal">
        <div class="modal-content">
            <h3>Inject Prompt</h3>
            <p style="margin-bottom:10px;color:#888;font-size:13px">Sending to: <strong id="inject-target"></strong></p>
            <textarea id="inject-prompt" placeholder="Enter instruction for Claude..."></textarea>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeModal()">Cancel</button>
                <button class="btn" onclick="sendCommand()">Send</button>
            </div>
        </div>
    </div>

    <script>
        let currentSessionId = null;

        async function fetchData() {
            try {
                const [statsRes, instancesRes, eventsRes] = await Promise.all([
                    fetch('/api/stats'),
                    fetch('/api/instances'),
                    fetch('/api/events?limit=50')
                ]);

                const stats = await statsRes.json();
                const { instances } = await instancesRes.json();
                const { events } = await eventsRes.json();

                updateStats(stats);
                updateInstances(instances);
                updateEvents(events);
            } catch (e) {
                console.error('Fetch error:', e);
            }
        }

        function updateStats(stats) {
            document.getElementById('active-count').textContent = stats.activeInstances;
            document.getElementById('event-count').textContent = stats.totalEvents;
            document.getElementById('uptime').textContent = formatUptime(stats.uptime);
        }

        function formatUptime(seconds) {
            if (seconds < 60) return Math.floor(seconds) + 's';
            if (seconds < 3600) return Math.floor(seconds / 60) + 'm';
            return Math.floor(seconds / 3600) + 'h';
        }

        function updateInstances(instances) {
            const container = document.getElementById('instances');
            if (!instances.length) {
                container.innerHTML = '<div class="empty">No instances connected yet</div>';
                return;
            }

            container.innerHTML = instances.map(i => \`
                <div class="instance-card \${i.status}">
                    <div class="instance-name">\${i.project}\${i.mode === 'standby' ? ' <span style="color:#fb923c;font-size:11px;background:rgba(251,146,60,0.2);padding:2px 6px;border-radius:3px;margin-left:8px">STANDBY</span>' : ''}</div>
                    <div class="instance-path">\${i.projectPath}</div>
                    <div class="instance-meta">
                        <span>Tools: \${i.toolCount}</span>
                        <span>Last: \${i.lastTool || 'N/A'}</span>
                        <span>Status: \${i.status}</span>
                    </div>
                    <div class="instance-actions">
                        <button class="btn" onclick="openInject('\${i.sessionId}', '\${i.project}')">Send Command</button>
                    </div>
                </div>
            \`).join('');
        }

        function updateEvents(events) {
            const container = document.getElementById('events');
            if (!events.length) {
                container.innerHTML = '<div class="empty">No events yet</div>';
                return;
            }

            container.innerHTML = events.map(e => \`
                <div class="event">
                    <span class="event-tool">\${e.tool || e.event}</span>
                    <span> in </span>
                    <strong>\${e.project}</strong>
                    <div class="event-time">\${new Date(e.timestamp * 1000).toLocaleTimeString()}</div>
                </div>
            \`).join('');
        }

        function openInject(sessionId, project) {
            currentSessionId = sessionId;
            document.getElementById('inject-target').textContent = project;
            document.getElementById('inject-prompt').value = '';
            document.getElementById('inject-modal').classList.add('active');
            document.getElementById('inject-prompt').focus();
        }

        function closeModal() {
            document.getElementById('inject-modal').classList.remove('active');
            currentSessionId = null;
        }

        async function sendCommand() {
            const prompt = document.getElementById('inject-prompt').value.trim();
            if (!prompt || !currentSessionId) return;

            try {
                await fetch('/api/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ sessionId: currentSessionId, prompt })
                });
                closeModal();
            } catch (e) {
                alert('Failed to send command');
            }
        }

        // Initial fetch
        fetchData();

        // Refresh every 3 seconds
        setInterval(fetchData, 3000);

        // Close modal on Escape
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') closeModal();
        });
    </script>
</body>
</html>`;
}

// Start server - bind to localhost by default for security
// Set MISSION_CONTROL_HOST=0.0.0.0 to allow network access
const server = http.createServer(handleRequest);
const HOST = process.env.MISSION_CONTROL_HOST || '127.0.0.1';

server.listen(PORT, HOST, () => {
    const networkIP = getLocalIP();
    console.log(`Mission Control v${SERVER_VERSION} running`);
    console.log(`  Local:   http://localhost:${PORT}/`);
    if (networkIP) {
        console.log(`  Network: http://${networkIP}:${PORT}/`);
    }
    console.log(`Press Ctrl+C to stop`);
});

/**
 * Get local network IP for display
 */
function getLocalIP() {
    const os = require('os');
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return null;
}

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down Mission Control...');
    server.close();
    process.exit(0);
});

process.on('SIGTERM', () => {
    server.close();
    process.exit(0);
});
