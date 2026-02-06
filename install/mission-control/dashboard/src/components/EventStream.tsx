import type { Event } from '../types'

const TOOL_ICONS: Record<string, string> = {
  Read: '\uD83D\uDCD6',
  Write: '\u270F\uFE0F',
  Edit: '\uD83D\uDCDD',
  Bash: '\uD83D\uDCBB',
  Grep: '\uD83D\uDD0D',
  Glob: '\uD83D\uDCC1',
  Skill: '\u26A1',
  Task: '\uD83E\uDD16',
  WebFetch: '\uD83C\uDF10',
  WebSearch: '\uD83D\uDD0E',
  SessionStart: '\uD83D\uDE80',
  Stop: '\uD83D\uDED1',
}

function formatTime(timestamp: number): string {
  const date = new Date(timestamp * 1000)
  const now = new Date()
  const diff = (now.getTime() - date.getTime()) / 1000

  if (diff < 60) return 'Just now'
  if (diff < 3600) return Math.floor(diff / 60) + 'm ago'
  if (diff < 86400) return Math.floor(diff / 3600) + 'h ago'
  return date.toLocaleDateString()
}

interface EventStreamProps {
  events: Event[]
}

export function EventStream({ events }: EventStreamProps) {
  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Event Stream</h2>
        <div className="connection-status">
          <div className="connection-dot" />
          <span>Live</span>
        </div>
      </div>
      <div className="panel-body">
        {events.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">{'\uD83D\uDCED'}</div>
            <div className="empty-title">No events yet</div>
            <div>Events will appear as instances report activity</div>
          </div>
        ) : (
          <div className="event-list">
            {events.slice(0, 50).map((e, i) => {
              const icon = TOOL_ICONS[e.tool] || TOOL_ICONS[e.event] || '\u2699\uFE0F'
              return (
                <div className="event" key={`${e.timestamp}-${i}`}>
                  <div className="event-left">
                    <div className="event-icon">{icon}</div>
                    <div>
                      <div className="event-tool">{e.tool || e.event}</div>
                      <div className="event-project">{e.project}</div>
                    </div>
                  </div>
                  <div className="event-time">{formatTime(e.timestamp)}</div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
