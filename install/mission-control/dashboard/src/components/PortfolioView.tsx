import type { Codebase, Instance } from '../types'
import { FOUNDATIONAL_ARTIFACTS, ARTIFACT_TYPE_ICONS } from '../types'

interface PortfolioViewProps {
  codebases: Codebase[]
  instances: Instance[]
  onSelectProject: (projectPath: string) => void
}

function formatRelativeTime(unixSeconds: number): string {
  const now = Date.now() / 1000
  const diff = now - unixSeconds
  if (diff < 60) return 'Just now'
  if (diff < 3600) return Math.floor(diff / 60) + 'm ago'
  if (diff < 86400) return Math.floor(diff / 3600) + 'h ago'
  if (diff < 604800) return Math.floor(diff / 86400) + 'd ago'
  return new Date(unixSeconds * 1000).toLocaleDateString()
}

function getFreshness(lastActivity: number, lastContext?: string): { color: string; label: string; className: string } {
  if (!lastActivity) {
    return { color: 'var(--text-disabled)', label: 'No activity', className: 'none' }
  }
  const diff = Date.now() / 1000 - lastActivity
  const timeStr = formatRelativeTime(lastActivity)
  const context = lastContext ? ` \u2014 ${lastContext}` : ''
  if (diff < 3600) return { color: 'var(--status-active)', label: `Fresh${context} ${timeStr}`, className: 'fresh' }
  if (diff < 86400) return { color: 'var(--status-standby)', label: `${timeStr}${context}`, className: 'recent' }
  return { color: 'var(--status-stale)', label: `${timeStr}${context}`, className: 'stale' }
}

function getSessionBadge(
  projectInstances: Instance[]
): { label: string; className: string } {
  if (projectInstances.length === 0) {
    return { label: 'No sessions', className: 'badge-none' }
  }

  const active = projectInstances.filter(i => i.status === 'active' && i.mode !== 'standby').length
  const standby = projectInstances.filter(i => i.mode === 'standby').length
  const stopped = projectInstances.filter(i => i.status === 'stopped').length

  const parts: string[] = []
  if (active > 0) parts.push(`${active} active`)
  if (standby > 0) parts.push(`${standby} standby`)
  if (stopped > 0 && active === 0 && standby === 0) parts.push(`${stopped} stopped`)

  const label = parts.join(' \u00B7 ') // middle dot separator

  // Pick the highest-priority status for badge color
  if (active > 0) return { label, className: 'badge-active' }
  if (standby > 0) return { label, className: 'badge-standby' }
  return { label, className: 'badge-stopped' }
}

function ProjectCard({
  codebase,
  projectInstances,
  onSelect,
}: {
  codebase: Codebase
  projectInstances: Instance[]
  onSelect: () => void
}) {
  const sessionBadge = getSessionBadge(projectInstances)

  // Find last used skill for context
  const lastSkill = Object.entries(codebase.skills)
    .sort(([, a], [, b]) => b.lastUsed - a.lastUsed)[0]
  const lastContext = lastSkill ? lastSkill[0].replace('shipkit-', '') : undefined
  const freshness = getFreshness(codebase.lastActivity, lastContext)
  const artifactCount = codebase.artifacts ? Object.keys(codebase.artifacts).length : 0
  const artifactTypes = codebase.artifacts
    ? new Set(Object.values(codebase.artifacts).map(a => a.type))
    : new Set<string>()

  // Count stale artifacts (> 7 days old)
  const staleCount = codebase.artifacts
    ? Object.values(codebase.artifacts).filter(a => {
        if (!a.lastUpdated) return false
        const updated = new Date(a.lastUpdated).getTime()
        return !isNaN(updated) && (Date.now() - updated) > 7 * 24 * 60 * 60 * 1000
      }).length
    : 0

  return (
    <div
      className="project-card"
      role="button"
      tabIndex={0}
      onClick={onSelect}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          onSelect()
        }
      }}
    >
      {/* Top row: name + session badge */}
      <div className="project-card-header">
        <h3>{codebase.projectName}</h3>
        <span className={`badge ${sessionBadge.className}`}>{sessionBadge.label}</span>
      </div>

      {/* Stats row */}
      <div className="project-card-stats">
        <span>{artifactCount} artifact{artifactCount !== 1 ? 's' : ''}</span>
        <span>{codebase.skillCount} skill{codebase.skillCount !== 1 ? 's' : ''} used</span>
        {staleCount > 0 && (
          <span className="badge badge-stale">{staleCount} stale</span>
        )}
        {codebase.lastActivity ? (
          <span>{formatRelativeTime(codebase.lastActivity)}</span>
        ) : (
          <span style={{ color: 'var(--text-dim)' }}>No activity</span>
        )}
      </div>

      {/* Artifact coverage row */}
      <div className="project-card-artifacts">
        {FOUNDATIONAL_ARTIFACTS.map((type) => {
          const exists = artifactTypes.has(type)
          return (
            <div
              key={type}
              className={`coverage-item ${exists ? 'exists' : 'missing'}`}
              title={`${type}: ${exists ? 'exists' : 'missing'}`}
            >
              <span className="coverage-dot">{ARTIFACT_TYPE_ICONS[type] ?? ''}</span>
              <span className="coverage-label">{type}</span>
            </div>
          )
        })}
      </div>

      {/* Freshness indicator */}
      <div className={`project-card-freshness ${freshness.className}`}>
        <span
          className="status-dot"
          style={{ background: freshness.color }}
        />
        <span>{freshness.label}</span>
      </div>
    </div>
  )
}

export function PortfolioView({ codebases, instances, onSelectProject }: PortfolioViewProps) {
  if (codebases.length === 0) {
    return (
      <div className="portfolio">
        <div className="empty-state">
          <div className="empty-state-icon">{'\uD83D\uDE80'}</div>
          <div className="empty-state-title">No projects yet</div>
          <div className="empty-state-text">
            Start a Claude Code session with Shipkit to see your projects here.
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="portfolio">
      <div className="portfolio-header">
        <h2>Your Projects</h2>
        <span className="project-count">
          {codebases.length} project{codebases.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="project-grid">
        {codebases.map((codebase) => {
          const projectInstances = instances.filter(
            (i) => i.projectPath === codebase.projectPath
          )
          return (
            <ProjectCard
              key={codebase.projectPath}
              codebase={codebase}
              projectInstances={projectInstances}
              onSelect={() => onSelectProject(codebase.projectPath)}
            />
          )
        })}
      </div>
    </div>
  )
}
