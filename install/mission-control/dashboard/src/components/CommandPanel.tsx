import { useState, useRef, useEffect } from 'react'
import { sendCommand, fetchQueue } from '../api'
import type { QueueStatus } from '../types'

const SKILL_CATEGORIES = [
  {
    label: 'Discovery',
    skills: [
      { skill: 'shipkit-project-status', label: 'Status', icon: '\uD83D\uDCCA' },
      { skill: 'shipkit-project-context', label: 'Context', icon: '\uD83D\uDD0D' },
      { skill: 'shipkit-codebase-index', label: 'Index', icon: '\uD83D\uDCC2' },
      { skill: 'shipkit-product-discovery', label: 'Discovery', icon: '\uD83D\uDC65' },
      { skill: 'shipkit-why-project', label: 'Why', icon: '\uD83E\uDD14' },
    ],
  },
  {
    label: 'Planning',
    skills: [
      { skill: 'shipkit-goals', label: 'Goals', icon: '\uD83C\uDFAF' },
      { skill: 'shipkit-spec', label: 'Spec', icon: '\uD83D\uDCC4' },
      { skill: 'shipkit-plan', label: 'Plan', icon: '\uD83D\uDCCB' },
      { skill: 'shipkit-feedback-bug', label: 'Bug', icon: '\uD83D\uDC1B' },
      { skill: 'shipkit-prototyping', label: 'Prototype', icon: '\uD83C\uDFA8' },
      { skill: 'shipkit-prototype-to-spec', label: 'Proto\u2192Spec', icon: '\uD83D\uDD04' },
      { skill: 'shipkit-thinking-partner', label: 'Think', icon: '\uD83E\uDDE0' },
    ],
  },
  {
    label: 'Knowledge',
    skills: [
      { skill: 'shipkit-architecture-memory', label: 'Arch', icon: '\uD83C\uDFD7\uFE0F' },
      { skill: 'shipkit-data-contracts', label: 'Contracts', icon: '\uD83D\uDD17' },
      { skill: 'shipkit-integration-docs', label: 'Docs', icon: '\uD83D\uDCDA' },
      { skill: 'shipkit-work-memory', label: 'Memory', icon: '\uD83D\uDCDD' },
      { skill: 'shipkit-user-instructions', label: 'Tasks', icon: '\u2705' },
    ],
  },
  {
    label: 'Execution',
    skills: [
      { skill: 'shipkit-build-relentlessly', label: 'Build', icon: '\uD83D\uDD28' },
      { skill: 'shipkit-test-relentlessly', label: 'Test', icon: '\uD83E\uDDEA' },
      { skill: 'shipkit-lint-relentlessly', label: 'Lint', icon: '\u2728' },
      { skill: 'shipkit-implement-independently', label: 'Implement', icon: '\u2699\uFE0F' },
      { skill: 'shipkit-test-cases', label: 'Cases', icon: '\uD83D\uDCCB' },
    ],
  },
  {
    label: 'Quality',
    skills: [
      { skill: 'shipkit-verify', label: 'Verify', icon: '\u2705' },
      { skill: 'shipkit-preflight', label: 'Preflight', icon: '\uD83D\uDE80' },
      { skill: 'shipkit-scale-ready', label: 'Scale', icon: '\uD83D\uDCC8' },
      { skill: 'shipkit-prompt-audit', label: 'Prompts', icon: '\uD83D\uDD0D' },
      { skill: 'shipkit-ux-audit', label: 'UX', icon: '\uD83C\uDFA8' },
    ],
  },
  {
    label: 'Communication',
    skills: [
      { skill: 'shipkit-communications', label: 'Comms', icon: '\uD83D\uDCE8' },
      { skill: 'shipkit-master', label: 'Master', icon: '\uD83D\uDC51' },
    ],
  },
  {
    label: 'System',
    skills: [
      { skill: 'shipkit-standby', label: 'Standby', icon: '\uD83D\uDCE1' },
      { skill: 'shipkit-update', label: 'Update', icon: '\u2B06\uFE0F' },
      { skill: 'shipkit-detect', label: 'Detect', icon: '\uD83D\uDD2C' },
      { skill: 'shipkit-mission-control', label: 'Mission', icon: '\uD83D\uDCE1' },
      { skill: 'shipkit-get-skills', label: 'Skills', icon: '\uD83D\uDCC3' },
      { skill: 'shipkit-get-mcps', label: 'MCPs', icon: '\uD83D\uDD0C' },
      { skill: 'shipkit-cleanup-worktrees', label: 'Cleanup', icon: '\uD83E\uDDF9' },
    ],
  },
]

interface CommandPanelProps {
  sessionId: string
  project: string
  onClose: () => void
  hasActiveSession?: boolean
}

export function CommandPanel({ sessionId, project, onClose, hasActiveSession = true }: CommandPanelProps) {
  const [selectedSkill, setSelectedSkill] = useState<string | null>(null)
  const [freeText, setFreeText] = useState('')
  const [sending, setSending] = useState(false)
  const [sent, setSent] = useState<{ commandId: string; prompt: string } | null>(null)
  const [queue, setQueue] = useState<QueueStatus | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Fetch queue status on open and after sending
  useEffect(() => {
    fetchQueue(sessionId).then(setQueue).catch(() => {})
  }, [sessionId, sent])

  // Escape key closes modal
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [onClose])

  function buildPrompt(): string {
    const parts: string[] = []
    if (selectedSkill) parts.push(`/${selectedSkill}`)
    if (freeText.trim()) parts.push(freeText.trim())
    return parts.join(' ')
  }

  const canSend = selectedSkill || freeText.trim()

  async function handleSend() {
    const prompt = buildPrompt()
    if (!prompt || sending) return

    setSending(true)
    try {
      const result = await sendCommand(sessionId, prompt)
      setSent({ commandId: result.commandId, prompt })
      setSelectedSkill(null)
      setFreeText('')
      // Auto-dismiss confirmation after 3s
      setTimeout(() => setSent(null), 3000)
    } catch {
      // Stay on modal so user can retry
    } finally {
      setSending(false)
    }
  }

  function handleSkillClick(skill: string) {
    if (selectedSkill === skill) {
      setSelectedSkill(null)
    } else {
      setSelectedSkill(skill)
      textareaRef.current?.focus()
    }
  }

  async function handleQuickSend(skill: string) {
    setSending(true)
    try {
      const result = await sendCommand(sessionId, `/${skill}`, 'Mission Control Quick Skill')
      setSent({ commandId: result.commandId, prompt: `/${skill}` })
      setTimeout(() => setSent(null), 3000)
    } catch {
      // ignore
    } finally {
      setSending(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSend()
    }
  }

  const pendingCount = (queue?.pending.length ?? 0) + (queue?.inflight.length ?? 0)

  return (
    <div className="modal-overlay" onClick={e => { if (e.target === e.currentTarget) onClose() }}>
      <div className="modal-content">
        <div className="modal-header">
          <h3>Send Command</h3>
          <button className="btn btn-ghost" onClick={onClose}>&times;</button>
        </div>

        <div className="command-target">
          Sending to: <strong>{project}</strong>
          {pendingCount > 0 && (
            <span className="badge">{pendingCount} in queue</span>
          )}
        </div>

        {!hasActiveSession && (
          <div className="command-info">
            No active session — commands will be queued and picked up when a session starts.
          </div>
        )}

        {/* Sent confirmation */}
        {sent && (
          <div className="command-sent">
            Queued: <code>{sent.prompt.substring(0, 80)}{sent.prompt.length > 80 ? '...' : ''}</code>
          </div>
        )}

        {/* Skill picker */}
        <div className="command-skills">
          {SKILL_CATEGORIES.map(cat => (
            <div key={cat.label} className="skill-category">
              <div className="skill-category-label">{cat.label}</div>
              <div className="skill-chips">
                {cat.skills.map(s => (
                  <button
                    key={s.skill}
                    className={`skill-chip ${selectedSkill === s.skill ? 'selected' : ''}`}
                    onClick={() => handleSkillClick(s.skill)}
                    onDoubleClick={() => handleQuickSend(s.skill)}
                    title={`Click to select, double-click to send immediately\n/${s.skill}`}
                  >
                    <span className="chip-icon">{s.icon}</span>
                    <span>{s.label}</span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Free text input */}
        <div className="command-input">
          {selectedSkill && (
            <div className="command-skill-tag">
              /{selectedSkill}
              <button className="btn btn-ghost" onClick={() => setSelectedSkill(null)}>&times;</button>
            </div>
          )}
          <textarea
            ref={textareaRef}
            value={freeText}
            onChange={e => setFreeText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={selectedSkill
              ? 'Add context or arguments (optional)...'
              : 'Type a free-text instruction for Claude...'}
          />
        </div>

        {/* Queue status */}
        {queue && queue.total > 0 && (
          <div className="command-queue">
            {queue.pending.length > 0 && (
              <span className="badge">{queue.pending.length} pending</span>
            )}
            {queue.inflight.length > 0 && (
              <span className="badge">{queue.inflight.length} inflight</span>
            )}
            {queue.processed.length > 0 && (
              <span className="badge">{queue.processed.length} processed</span>
            )}
          </div>
        )}

        <div className="modal-actions">
          <div className="command-hint">Ctrl+Enter to send</div>
          <div className="command-buttons">
            <button className="btn btn-secondary" onClick={onClose}>Close</button>
            <button className="btn btn-primary" onClick={handleSend} disabled={!canSend || sending}>
              {sending ? 'Sending...' : hasActiveSession ? 'Send Command' : 'Queue Command'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
