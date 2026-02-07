import { useState } from 'react'
import type { Event, Instance } from '../types'

interface ProjectActivityProps {
  events: Event[]
  instances: Instance[]
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

type ActivityFilter = 'all' | 'skills'

export function ProjectActivity({ events, instances }: ProjectActivityProps) {
  const [filter, setFilter] = useState<ActivityFilter>('all')

  // Apply filter
  const filteredEvents = filter === 'skills'
    ? events.filter(e => e.skill || e.tool === 'Skill')
    : events

  // Group events by sessionId
  const sessionGroups: Map<string, Event[]> = new Map()
  for (const evt of filteredEvents) {
    const group = sessionGroups.get(evt.sessionId)
    if (group) {
      group.push(evt)
    } else {
      sessionGroups.set(evt.sessionId, [evt])
    }
  }

  // Build a lookup for instance metadata
  const instanceMap = new Map<string, Instance>()
  for (const inst of instances) {
    instanceMap.set(inst.sessionId, inst)
  }

  if (events.length === 0) {
    return (
      <div className="activity-timeline">
        <div className="empty-state">
          <div className="empty-state-icon">{'\uD83D\uDCCB'}</div>
          <div className="empty-state-title">No activity recorded yet for this project</div>
        </div>
      </div>
    )
  }

  return (
    <div className="activity-timeline">
      {/* Filter bar */}
      <div className="activity-filter">
        <button
          className={`activity-filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Events
        </button>
        <button
          className={`activity-filter-btn ${filter === 'skills' ? 'active' : ''}`}
          onClick={() => setFilter('skills')}
        >
          Skills Only
        </button>
      </div>

      {/* Session groups */}
      {Array.from(sessionGroups.entries()).map(([sessionId, sessionEvents]) => {
        const instance = instanceMap.get(sessionId)
        const statusClass = instance?.status ?? 'stopped'
        const statusLabel = instance?.mode === 'standby'
          ? 'Standby'
          : instance?.status === 'active'
            ? 'Active'
            : instance?.status === 'stale'
              ? 'Stale'
              : 'Stopped'
        const badgeClass = instance?.mode === 'standby'
          ? 'badge-standby'
          : instance?.status === 'active'
            ? 'badge-active'
            : 'badge-stopped'

        return (
          <div key={sessionId} className="session-group">
            <div className="session-group-header">
              <div className="session-group-id">
                <span className={`mini-status-dot ${statusClass}`} />
                <span className="session-id-text">{sessionId.substring(0, 8)}</span>
                <span className={`badge ${badgeClass}`}>{statusLabel}</span>
              </div>
              <span className="session-event-count">
                {sessionEvents.length} event{sessionEvents.length !== 1 ? 's' : ''}
              </span>
            </div>

            <div className="session-events">
              {sessionEvents.map((evt, i) => (
                <div key={i} className="activity-event">
                  <span className="activity-event-icon">
                    {TOOL_ICONS[evt.tool] ?? '\u2022'}
                  </span>
                  <span className="activity-event-tool">{evt.tool}</span>
                  {evt.skill && (
                    <span className="activity-event-skill">{evt.skill}</span>
                  )}
                  <span className="activity-event-time">{formatRelativeTime(evt.timestamp)}</span>
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}
