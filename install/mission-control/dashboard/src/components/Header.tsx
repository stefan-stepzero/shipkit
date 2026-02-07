import type { Stats } from '../types'

interface HeaderProps {
  stats: Stats | null
}

export function Header({ stats }: HeaderProps) {
  return (
    <div className="header">
      <div className="header-left">
        <h1>Mission Control</h1>
        <div className="header-subtitle">Shipkit Multi-Instance Monitor</div>
      </div>
      <div className="stats">
        <div className="stat">
          <div className="stat-value">{stats?.activeInstances ?? 0}</div>
          <div className="stat-label">Active</div>
        </div>
        <div className="stat">
          <div className="stat-value">{stats?.totalInstances ?? 0}</div>
          <div className="stat-label">Total</div>
        </div>
        <div className="stat">
          <div className="stat-value">{stats?.totalEvents ?? 0}</div>
          <div className="stat-label">Events</div>
        </div>
      </div>
    </div>
  )
}
