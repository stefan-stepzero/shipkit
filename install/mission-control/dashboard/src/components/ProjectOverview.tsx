import { useState } from 'react'
import type { Codebase, Instance, Event } from '../types'
import { FOUNDATIONAL_ARTIFACTS, PER_FEATURE_ARTIFACTS, QUALITY_ARTIFACTS, ALL_ARTIFACT_TYPES, ARTIFACT_TYPE_ICONS } from '../types'

interface ProjectOverviewProps {
  codebase: Codebase
  instances: Instance[]
  events: Event[]
}

const TOOL_ICONS: Record<string, string> = {
  Read: '\uD83D\uDCD6', Write: '\u270F\uFE0F', Edit: '\uD83D\uDCDD',
  Bash: '\uD83D\uDCBB', Grep: '\uD83D\uDD0D', Glob: '\uD83D\uDCC1',
  Skill: '\u26A1', Task: '\uD83E\uDD16', WebFetch: '\uD83C\uDF10',
  WebSearch: '\uD83D\uDD0E', SessionStart: '\uD83D\uDE80', Stop: '\uD83D\uDED1',
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

function formatTypeName(type: string): string {
  return type.replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase())
}

function getArtifactAge(lastUpdated: string): string {
  const updated = new Date(lastUpdated).getTime()
  if (isNaN(updated)) return ''
  const diffMs = Date.now() - updated
  const diffMin = Math.floor(diffMs / 60000)
  if (diffMin < 60) return `${diffMin}m ago`
  const diffHr = Math.floor(diffMin / 60)
  if (diffHr < 24) return `${diffHr}h ago`
  const diffDays = Math.floor(diffHr / 24)
  return `${diffDays}d ago`
}

function isStaleArtifact(lastUpdated: string): boolean {
  const updated = new Date(lastUpdated).getTime()
  if (isNaN(updated)) return false
  const diffMs = Date.now() - updated
  const diffDays = diffMs / (1000 * 60 * 60 * 24)
  return diffDays > 7
}

export function ProjectOverview({ codebase, instances, events }: ProjectOverviewProps) {
  const [showAllArtifacts, setShowAllArtifacts] = useState(false)

  const activeCount = instances.filter(i => i.status === 'active').length
  const artifactCount = codebase.artifacts ? Object.keys(codebase.artifacts).length : 0

  const foundationalSet = new Set<string>(FOUNDATIONAL_ARTIFACTS)
  const perFeatureSet = new Set<string>(PER_FEATURE_ARTIFACTS)
  const qualitySet = new Set<string>(QUALITY_ARTIFACTS)

  // Skill usage sorted by most used
  const skillEntries = Object.values(codebase.skills)
    .sort((a, b) => b.useCount - a.useCount)

  // Artifact data
  const existingArtifacts = codebase.artifacts
    ? Object.entries(codebase.artifacts)
    : []

  const existingTypes = new Set(existingArtifacts.map(([, a]) => a.type))

  // Categorize existing artifacts
  const foundationArtifacts = existingArtifacts.filter(([, a]) => foundationalSet.has(a.type))
  const featureArtifacts = existingArtifacts.filter(([, a]) => perFeatureSet.has(a.type))
  const qualityArtifacts = existingArtifacts.filter(([, a]) => qualitySet.has(a.type))
  const contextArtifacts = existingArtifacts.filter(([, a]) =>
    !foundationalSet.has(a.type) && !perFeatureSet.has(a.type) && !qualitySet.has(a.type)
  )

  const missingFoundational = FOUNDATIONAL_ARTIFACTS.filter(
    f => !existingTypes.has(f)
  )

  const isCollapsed = artifactCount <= 3 && !showAllArtifacts

  return (
    <div className="overview">
      {/* 1. Project Health (compact stats) */}
      <div className="overview-stats-compact">
        <span>{activeCount} sessions</span>
        <span className="stats-sep">&middot;</span>
        <span>{artifactCount} artifacts</span>
        <span className="stats-sep">&middot;</span>
        <span>{codebase.skillCount} skills used</span>
        <span className="stats-sep">&middot;</span>
        <span>{events.length} events</span>
      </div>

      {/* 3. Artifacts (smart summary) */}
      <div className="overview-section">
        <div className="overview-section-title">Artifacts</div>
        {isCollapsed ? (
          <div className="artifact-summary">
            <div className="artifact-summary-header">
              <span>Artifacts: {artifactCount} of {ALL_ARTIFACT_TYPES.length}</span>
              <button
                className="btn btn-ghost"
                onClick={() => setShowAllArtifacts(true)}
              >
                View all &rarr;
              </button>
            </div>
            {existingArtifacts.length > 0 && (
              <div className="artifact-summary-list">
                {existingArtifacts.map(([key, artifact]) => {
                  const age = getArtifactAge(artifact.lastUpdated)
                  const stale = isStaleArtifact(artifact.lastUpdated)
                  return (
                    <div key={key} className="artifact-summary-item">
                      <span>{ARTIFACT_TYPE_ICONS[artifact.type] ?? '\uD83D\uDCC4'}</span>
                      <span>{formatTypeName(artifact.type)}</span>
                      {age && (
                        <span className={`artifact-age${stale ? ' stale' : ''}`}>
                          ({age})
                        </span>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
            {missingFoundational.length > 0 && (
              <div className="artifact-summary-missing">
                Missing foundational: {missingFoundational.map(f => formatTypeName(f)).join(', ')}
              </div>
            )}
          </div>
        ) : (
          <div className="artifact-summary">
            {artifactCount > 3 && (
              <div className="artifact-summary-header">
                <span>Artifacts: {artifactCount} of {ALL_ARTIFACT_TYPES.length}</span>
                <button
                  className="btn btn-ghost"
                  onClick={() => setShowAllArtifacts(false)}
                >
                  Collapse
                </button>
              </div>
            )}

            {/* Foundation — project-wide, most skills depend on these */}
            <div className="coverage-category">
              <div className="coverage-category-label">Foundation ({foundationArtifacts.length}/{FOUNDATIONAL_ARTIFACTS.length})</div>
              <div className="coverage-grid">
                {foundationArtifacts.map(([key, artifact]) => {
                  const age = getArtifactAge(artifact.lastUpdated)
                  const stale = isStaleArtifact(artifact.lastUpdated)
                  return (
                    <div key={key} className="coverage-item exists foundational" title={`${formatTypeName(artifact.type)}: exists`}>
                      <span className="coverage-icon">{ARTIFACT_TYPE_ICONS[artifact.type] ?? '\uD83D\uDCC4'}</span>
                      <span className="coverage-name">{formatTypeName(artifact.type)}</span>
                      <span className="coverage-status">{'\u2713'}</span>
                      {age && <span className={`artifact-age${stale ? ' stale' : ''}`}>{age}</span>}
                    </div>
                  )
                })}
                {missingFoundational.map(type => (
                  <div key={type} className="coverage-item missing foundational" title={`${formatTypeName(type)}: missing`}>
                    <span className="coverage-icon">{ARTIFACT_TYPE_ICONS[type] ?? '\uD83D\uDCC4'}</span>
                    <span className="coverage-name">{formatTypeName(type)}</span>
                    <span className="coverage-status">{'\u2014'}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Per-feature — specs, plans, bugs */}
            {featureArtifacts.length > 0 && (
              <div className="coverage-category">
                <div className="coverage-category-label">Features ({featureArtifacts.length} active)</div>
                <div className="coverage-grid">
                  {featureArtifacts.map(([key, artifact]) => {
                    const age = getArtifactAge(artifact.lastUpdated)
                    const stale = isStaleArtifact(artifact.lastUpdated)
                    return (
                      <div key={key} className="coverage-item exists" title={`${formatTypeName(artifact.type)}: ${key}`}>
                        <span className="coverage-icon">{ARTIFACT_TYPE_ICONS[artifact.type] ?? '\uD83D\uDCC4'}</span>
                        <span className="coverage-name">{key.replace('.json', '')}</span>
                        <span className="coverage-status">{'\u2713'}</span>
                        {age && <span className={`artifact-age${stale ? ' stale' : ''}`}>{age}</span>}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Quality gates */}
            {qualityArtifacts.length > 0 && (
              <div className="coverage-category">
                <div className="coverage-category-label">Quality Gates ({qualityArtifacts.length})</div>
                <div className="coverage-grid">
                  {qualityArtifacts.map(([key, artifact]) => {
                    const age = getArtifactAge(artifact.lastUpdated)
                    const stale = isStaleArtifact(artifact.lastUpdated)
                    return (
                      <div key={key} className="coverage-item exists" title={`${formatTypeName(artifact.type)}: exists`}>
                        <span className="coverage-icon">{ARTIFACT_TYPE_ICONS[artifact.type] ?? '\uD83D\uDCC4'}</span>
                        <span className="coverage-name">{formatTypeName(artifact.type)}</span>
                        <span className="coverage-status">{'\u2713'}</span>
                        {age && <span className={`artifact-age${stale ? ' stale' : ''}`}>{age}</span>}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Context & progress */}
            {contextArtifacts.length > 0 && (
              <div className="coverage-category">
                <div className="coverage-category-label">Context ({contextArtifacts.length})</div>
                <div className="coverage-grid">
                  {contextArtifacts.map(([key, artifact]) => {
                    const age = getArtifactAge(artifact.lastUpdated)
                    const stale = isStaleArtifact(artifact.lastUpdated)
                    return (
                      <div key={key} className="coverage-item exists" title={`${formatTypeName(artifact.type)}: exists`}>
                        <span className="coverage-icon">{ARTIFACT_TYPE_ICONS[artifact.type] ?? '\uD83D\uDCC4'}</span>
                        <span className="coverage-name">{formatTypeName(artifact.type)}</span>
                        <span className="coverage-status">{'\u2713'}</span>
                        {age && <span className={`artifact-age${stale ? ' stale' : ''}`}>{age}</span>}
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 4. Recent Activity (last 5, full context) */}
      <div className="overview-section">
        <div className="overview-section-title">Recent Activity</div>
        {events.length > 0 ? (
          <div className="activity-feed">
            {events.slice(0, 5).map((evt, i) => (
              <div key={i} className="activity-item">
                <span className="activity-item-icon">
                  {TOOL_ICONS[evt.tool] ?? '\u2022'}
                </span>
                <span className="activity-item-tool">{evt.tool}</span>
                {evt.skill && (
                  <span className="activity-item-skill">{evt.skill}</span>
                )}
                <span className="activity-item-time">{formatRelativeTime(evt.timestamp)}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-title">No activity yet</div>
            <div className="empty-state-text">Run a skill to see events here.</div>
          </div>
        )}
      </div>

      {/* 5. Skill Usage (unchanged, only if entries exist) */}
      {skillEntries.length > 0 && (
        <div className="overview-section">
          <div className="overview-section-title">Skill Usage</div>
          <div className="skill-usage-list">
            {skillEntries.map(skill => (
              <div key={skill.name} className="skill-usage-item">
                <span className="skill-usage-name">{skill.name}</span>
                <span className="badge">{skill.useCount}</span>
                <span className="skill-usage-time">{formatRelativeTime(skill.lastUsed)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
