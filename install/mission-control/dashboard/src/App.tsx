import { useState, useEffect } from 'react'
import { useDashboardData } from './hooks/useApi'
import { PortfolioView } from './components/PortfolioView'
import { ProjectDetail } from './components/ProjectDetail'
import type { AppRoute, Stats } from './types'

function parseRoute(): AppRoute {
  const hash = window.location.hash.slice(1) // remove #
  if (hash.startsWith('/project/')) {
    const projectPath = decodeURIComponent(hash.slice('/project/'.length))
    return { view: 'project', projectPath }
  }
  return { view: 'portfolio' }
}

function navigate(route: AppRoute) {
  if (route.view === 'portfolio') {
    window.location.hash = '#/'
  } else {
    window.location.hash = '#/project/' + encodeURIComponent(route.projectPath)
  }
}

function AppHeader({ stats, route, projectName }: {
  stats: Stats | null
  route: AppRoute
  projectName?: string
}) {
  return (
    <header className="app-header">
      <div className="app-header-left">
        <div className="app-logo" onClick={() => navigate({ view: 'portfolio' })} style={{ cursor: 'pointer' }}>
          <span className="app-logo-icon">{'\uD83D\uDE80'}</span>
          <span className="app-logo-text">Mission Control</span>
        </div>
        {route.view === 'project' && projectName && (
          <nav className="app-breadcrumb">
            <span className="breadcrumb-separator">/</span>
            <span className="breadcrumb-current">{projectName}</span>
          </nav>
        )}
      </div>
      <div className="app-header-right">
        <div className="app-header-stats">
          <div className="header-stat">
            <span className="header-stat-value">{stats?.activeInstances ?? 0}</span>
            <span className="header-stat-label">Active</span>
          </div>
          <div className="header-stat">
            <span className="header-stat-value">{stats?.totalCodebases ?? 0}</span>
            <span className="header-stat-label">Projects</span>
          </div>
          <div className="header-stat">
            <span className="header-stat-value">{stats?.totalEvents ?? 0}</span>
            <span className="header-stat-label">Events</span>
          </div>
        </div>
        <div className="connection-indicator">
          <span className="connection-dot" />
          <span>Live</span>
        </div>
      </div>
    </header>
  )
}

export default function App() {
  const { stats, instances, events, codebases, loading, error } = useDashboardData()
  const [route, setRoute] = useState<AppRoute>(parseRoute)

  // Listen for hash changes
  useEffect(() => {
    function onHashChange() {
      setRoute(parseRoute())
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  // Auto-redirect: if only one codebase, skip portfolio
  useEffect(() => {
    if (route.view === 'portfolio' && codebases.length === 1 && !loading) {
      navigate({ view: 'project', projectPath: codebases[0].projectPath })
    }
  }, [route.view, codebases, loading])

  // Find current project data
  const currentProject = route.view === 'project'
    ? codebases.find(c => c.projectPath === route.projectPath)
    : undefined

  const projectInstances = route.view === 'project'
    ? instances.filter(i => i.projectPath === route.projectPath)
    : []

  const projectEvents = route.view === 'project'
    ? events.filter(e => e.projectPath === route.projectPath)
    : []

  if (error) {
    return (
      <div className="app">
        <AppHeader stats={null} route={{ view: 'portfolio' }} />
        <main className="app-content">
          <div className="empty-state">
            <div className="empty-state-icon">{'\u26A0\uFE0F'}</div>
            <div className="empty-state-title">Connection Error</div>
            <div className="empty-state-text">{error}</div>
            <div className="empty-state-text" style={{ marginTop: 8, fontSize: 12 }}>
              Make sure Mission Control server is running on port 7777
            </div>
          </div>
        </main>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="app">
        <AppHeader stats={null} route={{ view: 'portfolio' }} />
        <main className="app-content">
          <div className="empty-state">
            <div className="empty-state-icon">{'\u23F3'}</div>
            <div className="empty-state-title">Connecting...</div>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="app">
      <AppHeader
        stats={stats}
        route={route}
        projectName={currentProject?.projectName}
      />
      <main className="app-content">
        {route.view === 'portfolio' && (
          <PortfolioView
            codebases={codebases}
            instances={instances}
            onSelectProject={(projectPath) => navigate({ view: 'project', projectPath })}
          />
        )}
        {route.view === 'project' && (
          <ProjectDetail
            codebase={currentProject ?? null}
            instances={projectInstances}
            events={projectEvents}
            onBack={() => navigate({ view: 'portfolio' })}
          />
        )}
      </main>
    </div>
  )
}
