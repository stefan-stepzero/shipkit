import { useState } from 'react'
import type { Codebase, Instance, Event } from '../types'
import { ProjectOverview } from './ProjectOverview'
import { ArtifactsView } from './ArtifactsView'
import { ProjectActivity } from './ProjectActivity'
import { CommandPanel } from './CommandPanel'

type ProjectTab = 'overview' | 'artifacts' | 'activity'

interface ProjectDetailProps {
  codebase: Codebase | null
  instances: Instance[]
  events: Event[]
  onBack: () => void
}

export function ProjectDetail({ codebase, instances, events, onBack }: ProjectDetailProps) {
  const [tab, setTab] = useState<ProjectTab>('overview')
  const [showCommand, setShowCommand] = useState(false)

  if (!codebase) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">{'\uD83D\uDD0D'}</div>
        <div className="empty-state-title">Project not found</div>
        <button className="btn btn-secondary" onClick={onBack}>{'\u2190'} Back to projects</button>
      </div>
    )
  }

  const activeSession = instances.find(i => i.status === 'active')
  const hasActiveSession = !!activeSession

  // Session status
  let sessionStatus: { label: string; className: string }
  if (instances.some(i => i.mode === 'standby')) {
    sessionStatus = { label: 'Standby', className: 'badge-standby' }
  } else if (instances.some(i => i.status === 'active')) {
    sessionStatus = { label: `${instances.filter(i => i.status === 'active').length} Active`, className: 'badge-active' }
  } else if (instances.some(i => i.status === 'stopped')) {
    sessionStatus = { label: 'Stopped', className: 'badge-stopped' }
  } else {
    sessionStatus = { label: 'No sessions', className: 'badge-none' }
  }

  const tabs: { key: ProjectTab; label: string }[] = [
    { key: 'overview', label: 'Overview' },
    { key: 'artifacts', label: `Artifacts${codebase.artifacts ? ` (${Object.keys(codebase.artifacts).length})` : ''}` },
    { key: 'activity', label: `Activity${events.length > 0 ? ` (${events.length})` : ''}` },
  ]

  return (
    <div className="project-detail">
      <div className="project-detail-header">
        <button className="btn btn-ghost" onClick={onBack}>
          {'\u2190'} All Projects
        </button>
        <div className="project-detail-title">
          <h1>{codebase.projectName}</h1>
          <span className="project-detail-path">{codebase.projectPath}</span>
        </div>
        <div className="project-detail-actions">
          <span className={`badge ${sessionStatus.className}`}>{sessionStatus.label}</span>
          <button
            className="btn btn-primary"
            onClick={() => setShowCommand(true)}
            title="Send a command to this project"
          >
            Send Command
          </button>
        </div>
      </div>

      <div className="project-tabs">
        {tabs.map(t => (
          <button
            key={t.key}
            className={`project-tab ${tab === t.key ? 'active' : ''}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="project-tab-content">
        {tab === 'overview' && (
          <ProjectOverview
            codebase={codebase}
            instances={instances}
            events={events}
          />
        )}
        {tab === 'artifacts' && (
          <ArtifactsView codebases={[codebase]} />
        )}
        {tab === 'activity' && (
          <ProjectActivity events={events} instances={instances} />
        )}
      </div>

      {showCommand && (
        <CommandPanel
          sessionId={activeSession?.sessionId ?? `project:${codebase.projectPath}`}
          project={codebase.projectName}
          onClose={() => setShowCommand(false)}
          hasActiveSession={hasActiveSession}
        />
      )}
    </div>
  )
}
