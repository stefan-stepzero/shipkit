import { useState } from 'react'
import { useDashboardData } from './hooks/useApi'
import { Header } from './components/Header'
import { InstancePanel } from './components/InstancePanel'
import { EventStream } from './components/EventStream'
import { InjectModal } from './components/InjectModal'
import { SkillsModal } from './components/SkillsModal'
import { ArtifactsView } from './components/ArtifactsView'

type View = 'dashboard' | 'artifacts'

export default function App() {
  const { stats, instances, events, codebases, error } = useDashboardData()
  const [view, setView] = useState<View>('dashboard')

  // Inject modal state
  const [injectTarget, setInjectTarget] = useState<{ sessionId: string; project: string } | null>(null)

  // Skills modal state
  const [skillsTarget, setSkillsTarget] = useState<{ sessionId: string; project: string } | null>(null)

  if (error) {
    return (
      <div className="empty" style={{ paddingTop: '20vh' }}>
        <div className="empty-icon">&#x26A0;&#xFE0F;</div>
        <div className="empty-title">Connection Error</div>
        <div>{error}</div>
      </div>
    )
  }

  return (
    <>
      <Header stats={stats} />

      <div className="nav-tabs">
        <button
          className={`nav-tab ${view === 'dashboard' ? 'active' : ''}`}
          onClick={() => setView('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={`nav-tab ${view === 'artifacts' ? 'active' : ''}`}
          onClick={() => setView('artifacts')}
        >
          Artifacts
        </button>
      </div>

      {view === 'dashboard' && (
        <div className="container">
          <InstancePanel
            instances={instances}
            codebases={codebases}
            onInject={(sessionId, project) => setInjectTarget({ sessionId, project })}
            onSkills={(sessionId, project) => setSkillsTarget({ sessionId, project })}
          />
          <EventStream events={events} />
        </div>
      )}

      {view === 'artifacts' && (
        <ArtifactsView codebases={codebases} />
      )}

      {injectTarget && (
        <InjectModal
          sessionId={injectTarget.sessionId}
          project={injectTarget.project}
          onClose={() => setInjectTarget(null)}
        />
      )}

      {skillsTarget && (
        <SkillsModal
          sessionId={skillsTarget.sessionId}
          project={skillsTarget.project}
          codebases={codebases}
          onClose={() => setSkillsTarget(null)}
        />
      )}
    </>
  )
}
