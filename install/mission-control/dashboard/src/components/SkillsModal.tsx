import { useEffect } from 'react'
import type { Codebase } from '../types'
import { sendCommand } from '../api'

const ALL_SKILLS = [
  { skill: 'shipkit-project-status', label: 'Status', icon: '\uD83D\uDCCA' },
  { skill: 'shipkit-project-context', label: 'Context', icon: '\uD83D\uDD0D' },
  { skill: 'shipkit-spec', label: 'Spec', icon: '\uD83D\uDCC4' },
  { skill: 'shipkit-plan', label: 'Plan', icon: '\uD83D\uDCCB' },
  { skill: 'shipkit-build-relentlessly', label: 'Build', icon: '\uD83D\uDD28' },
  { skill: 'shipkit-test-relentlessly', label: 'Test', icon: '\uD83E\uDDEA' },
  { skill: 'shipkit-lint-relentlessly', label: 'Lint', icon: '\u2728' },
  { skill: 'shipkit-verify', label: 'Verify', icon: '\u2705' },
  { skill: 'shipkit-preflight', label: 'Preflight', icon: '\uD83D\uDE80' },
  { skill: 'shipkit-work-memory', label: 'Work Memory', icon: '\uD83D\uDCDD' },
  { skill: 'shipkit-architecture-memory', label: 'Arch Memory', icon: '\uD83C\uDFD7\uFE0F' },
  { skill: 'shipkit-thinking-partner', label: 'Think', icon: '\uD83E\uDDE0' },
]

interface SkillsModalProps {
  sessionId: string
  project: string
  codebases: Codebase[]
  onClose: () => void
}

export function SkillsModal({ sessionId, project, codebases, onClose }: SkillsModalProps) {
  const codebase = codebases.find(c => c.projectName === project)
  const quickActions = codebase?.quickActions ?? [
    { skill: 'shipkit-project-status', label: 'Status', icon: '\uD83D\uDCCA' },
    { skill: 'shipkit-work-memory', label: 'Log Progress', icon: '\uD83D\uDCDD' },
  ]
  const recs = codebase?.recommendations ?? []

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [onClose])

  async function runSkill(skillName: string) {
    await sendCommand(sessionId, `/${skillName}`, 'Mission Control Quick Skill')
    onClose()
  }

  return (
    <div className="modal-overlay" onClick={e => { if (e.target === e.currentTarget) onClose() }}>
      <div className="modal-content wide">
        <div className="modal-header">
          <h3>Quick Skill Actions</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-target">
          Sending to: <strong>{project}</strong>
        </div>

        <div className="skill-section">
          <div className="skill-section-title">Quick Actions</div>
          <div className="skill-grid">
            {quickActions.map(a => (
              <button key={a.skill} className="skill-btn" onClick={() => runSkill(a.skill)}>
                <div className="icon">{a.icon}</div>
                <div className="name">{a.label}</div>
              </button>
            ))}
          </div>
        </div>

        {recs.length > 0 && (
          <div className="skill-section">
            <div className="skill-section-title" style={{ color: 'var(--accent-orange)' }}>
              Recommendations
            </div>
            {recs.map((r, i) => (
              <div className="recommendation-item" key={i}>
                <span className={`priority-${r.priority}`}>{'\u25CF'}</span>
                <span>{r.message}</span>
                <button className="rec-action" onClick={() => runSkill(r.skill)}>
                  Run
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="skill-section">
          <div className="skill-section-title">All Shipkit Skills</div>
          <div className="skill-grid">
            {ALL_SKILLS.map(s => (
              <button key={s.skill} className="skill-btn" onClick={() => runSkill(s.skill)}>
                <div className="icon">{s.icon}</div>
                <div className="name">{s.label}</div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
