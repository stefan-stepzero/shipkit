import type { Instance, Codebase } from '../types'
import { sendCommand } from '../api'

function formatTime(timestamp: number): string {
  const date = new Date(timestamp * 1000)
  const now = new Date()
  const diff = (now.getTime() - date.getTime()) / 1000

  if (diff < 60) return 'Just now'
  if (diff < 3600) return Math.floor(diff / 60) + 'm ago'
  if (diff < 86400) return Math.floor(diff / 3600) + 'h ago'
  return date.toLocaleDateString()
}

interface InstancePanelProps {
  instances: Instance[]
  codebases: Codebase[]
  onInject: (sessionId: string, project: string) => void
  onSkills: (sessionId: string, project: string) => void
}

interface CodebaseGroup {
  projectPath: string
  projectName: string
  instances: Instance[]
  codebase?: Codebase
}

export function InstancePanel({ instances, codebases, onInject, onSkills }: InstancePanelProps) {
  // Group instances by projectPath
  const grouped: Record<string, CodebaseGroup> = {}
  for (const instance of instances) {
    const path = instance.projectPath || 'Unknown'
    if (!grouped[path]) {
      grouped[path] = {
        projectPath: path,
        projectName: instance.project,
        instances: [],
        codebase: codebases.find(c => c.projectPath === path),
      }
    }
    grouped[path].instances.push(instance)
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Connected Instances</h2>
        <div className="connection-status">
          <div className="connection-dot" />
          <span>Live</span>
        </div>
      </div>
      <div className="panel-body">
        {instances.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">{'\uD83D\uDD0C'}</div>
            <div className="empty-title">No instances connected</div>
            <div>Start Claude Code in any project to see it here</div>
          </div>
        ) : (
          Object.values(grouped).map(group => (
            <CodebaseGroupCard
              key={group.projectPath}
              group={group}
              onInject={onInject}
              onSkills={onSkills}
            />
          ))
        )}
      </div>
    </div>
  )
}

function CodebaseGroupCard({
  group,
  onInject,
  onSkills,
}: {
  group: CodebaseGroup
  onInject: (sessionId: string, project: string) => void
  onSkills: (sessionId: string, project: string) => void
}) {
  const cb = group.codebase
  const recs = cb?.recommendations ?? []
  const skillCount = cb?.skillCount ?? 0

  return (
    <div className="codebase-group">
      <div className="codebase-header">
        <div>
          <div className="codebase-name">{group.projectName}</div>
          <div className="codebase-path">{group.projectPath}</div>
        </div>
        <div className="codebase-stats">
          <span>
            {'\uD83D\uDC65'} {group.instances.length} instance{group.instances.length > 1 ? 's' : ''}
          </span>
          <span>{'\u26A1'} {skillCount} skills used</span>
        </div>
      </div>

      <div className="codebase-instances">
        {group.instances.map(i => (
          <div className="mini-instance" key={i.sessionId}>
            <div className="mini-instance-info">
              <div className={`mini-status-dot ${i.status}`} />
              <div>
                <span style={{ fontWeight: 500 }}>{i.lastTool || 'Idle'}</span>
                <span style={{ color: 'var(--text-dim)', fontSize: 12 }}>
                  {' '}&middot; {formatTime(i.lastSeen)}
                </span>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <button
                className="btn btn-sm"
                onClick={() => onInject(i.sessionId, i.project)}
              >
                Inject
              </button>
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => onSkills(i.sessionId, i.project)}
              >
                Skills
              </button>
            </div>
          </div>
        ))}
      </div>

      {recs.length > 0 && (
        <div className="codebase-recommendations">
          <div style={{ fontSize: 11, color: 'var(--accent-orange)', marginBottom: 8, textTransform: 'uppercase' as const }}>
            Recommendations
          </div>
          {recs.slice(0, 3).map((r, i) => (
            <div className="recommendation-item" key={i}>
              <span className={`priority-${r.priority}`}>{'\u25CF'}</span>
              <span>{r.message}</span>
              <button
                className="rec-action"
                onClick={() => {
                  const sessionId = group.instances[0]?.sessionId
                  if (sessionId) sendCommand(sessionId, r.action, 'Mission Control Recommendation')
                }}
              >
                Run {r.action}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
