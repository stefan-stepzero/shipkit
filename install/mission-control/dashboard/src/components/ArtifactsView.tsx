import { useState } from 'react'
import type { Codebase, ArtifactData } from '../types'
import { ARTIFACT_TYPE_ICONS } from '../types'
import { ArtifactGraph } from './ArtifactGraph'
import { ArtifactStructuredView } from './ArtifactRenderers'

function formatSummaryValue(value: unknown): string {
  if (value === null || value === undefined) return '\u2014'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

// Artifacts that have graph visualization support
const GRAPH_ARTIFACTS = new Set(['architecture', 'data-contracts', 'product-discovery', 'prompt-audit'])
const STRUCTURED_ARTIFACTS = new Set([
  'goals', 'preflight', 'project-status', 'plan', 'spec', 'test-coverage',
  'work-memory', 'scale-readiness', 'bug-spec', 'prompt-audit', 'ux-decisions',
  'user-tasks', 'project-why', 'codebase-index'
])

const STALE_THRESHOLD_MS = 7 * 24 * 60 * 60 * 1000 // 7 days

function isStale(lastUpdated: string): boolean {
  const parsed = Date.parse(lastUpdated)
  if (isNaN(parsed)) return false
  return Date.now() - parsed > STALE_THRESHOLD_MS
}

interface ArtifactsViewProps {
  codebases: Codebase[]
}

export function ArtifactsView({ codebases }: ArtifactsViewProps) {
  const [selectedArtifact, setSelectedArtifact] = useState<{
    codebase: string
    filename: string
    data: ArtifactData
  } | null>(null)

  const codebasesWithArtifacts = codebases.filter(
    c => c.artifacts && Object.keys(c.artifacts).length > 0
  )

  if (codebasesWithArtifacts.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">{'\uD83D\uDCE6'}</div>
        <div className="empty-state-title">No artifacts received yet</div>
        <div className="empty-state-text">
          Run Shipkit skills in a project to generate .shipkit/*.json artifacts.
          The reporter hook will automatically send them here.
        </div>
      </div>
    )
  }

  if (selectedArtifact) {
    return (
      <ArtifactDetail
        codebase={selectedArtifact.codebase}
        filename={selectedArtifact.filename}
        data={selectedArtifact.data}
        onBack={() => setSelectedArtifact(null)}
      />
    )
  }

  // Single codebase (typical case) — show artifact grid directly
  if (codebasesWithArtifacts.length === 1) {
    const cb = codebasesWithArtifacts[0]
    const sortedArtifacts = getSortedArtifacts(cb)

    return (
      <div className="artifact-grid">
        {sortedArtifacts.map(([filename, data]) => (
          <ArtifactCard
            key={filename}
            filename={filename}
            data={data}
            hasGraph={GRAPH_ARTIFACTS.has(data.type)}
            stale={isStale(data.lastUpdated)}
            onClick={() => setSelectedArtifact({
              codebase: cb.projectName,
              filename,
              data,
            })}
          />
        ))}
      </div>
    )
  }

  // Multiple codebases (edge case) — show minimal codebase headers
  return (
    <div>
      {codebasesWithArtifacts.map(cb => {
        const sortedArtifacts = getSortedArtifacts(cb)

        return (
          <div key={cb.projectPath} className="artifact-codebase-group">
            <h3 className="artifact-codebase-header">{cb.projectName}</h3>
            <div className="artifact-grid">
              {sortedArtifacts.map(([filename, data]) => (
                <ArtifactCard
                  key={filename}
                  filename={filename}
                  data={data}
                  hasGraph={GRAPH_ARTIFACTS.has(data.type)}
                  stale={isStale(data.lastUpdated)}
                  onClick={() => setSelectedArtifact({
                    codebase: cb.projectName,
                    filename,
                    data,
                  })}
                />
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}

/** Sort artifacts by lastUpdated (most recent first), with unparseable dates last. */
function getSortedArtifacts(cb: Codebase): [string, ArtifactData][] {
  return Object.entries(cb.artifacts!).sort(([, a], [, b]) => {
    const aTime = Date.parse(a.lastUpdated)
    const bTime = Date.parse(b.lastUpdated)
    if (isNaN(aTime) && isNaN(bTime)) return 0
    if (isNaN(aTime)) return 1
    if (isNaN(bTime)) return -1
    return bTime - aTime
  })
}

function ArtifactCard({
  filename,
  data,
  hasGraph,
  stale,
  onClick,
}: {
  filename: string
  data: ArtifactData
  hasGraph: boolean
  stale: boolean
  onClick: () => void
}) {
  const icon = ARTIFACT_TYPE_ICONS[data.type] || '\uD83D\uDCC4'
  const summary = data.summary || {}
  const summaryEntries = Object.entries(summary).slice(0, 3)

  return (
    <div className="artifact-card" onClick={onClick}>
      <div className="artifact-card-header">
        <span className="artifact-card-icon">{icon}</span>
        <div className="artifact-card-badges">
          <span className="badge">{data.type}</span>
          {hasGraph && (
            <span className="badge badge-graph">graph</span>
          )}
          {!hasGraph && STRUCTURED_ARTIFACTS.has(data.type) && (
            <span className="badge badge-view">view</span>
          )}
          {stale && (
            <span className="badge badge-stale">stale</span>
          )}
        </div>
      </div>
      <h3>{filename}</h3>
      <div className="artifact-card-summary">
        {summaryEntries.map(([key, value]) => (
          <div key={key}>
            <span className="artifact-card-summary-key">{key}:</span>{' '}
            {formatSummaryValue(value)}
          </div>
        ))}
      </div>
      <div className="artifact-card-meta">
        {data.version && <span>v{data.version}</span>}
        {data.lastUpdated && <span>{data.lastUpdated}</span>}
        {data.source && <span>via {data.source}</span>}
      </div>
    </div>
  )
}

function ArtifactDetail({
  codebase,
  filename,
  data,
  onBack,
}: {
  codebase: string
  filename: string
  data: ArtifactData
  onBack: () => void
}) {
  const hasGraph = GRAPH_ARTIFACTS.has(data.type)
  const hasStructured = STRUCTURED_ARTIFACTS.has(data.type)
  const hasBothViews = hasGraph && hasStructured
  const hasRichView = hasGraph || hasStructured
  const [activeView, setActiveView] = useState<'graph' | 'structured' | 'json'>(
    hasGraph ? 'graph' : hasStructured ? 'structured' : 'json'
  )

  return (
    <div className="artifact-detail">
      <div className="artifact-detail-header">
        <button className="btn btn-secondary" onClick={onBack}>
          {'\u2190'} Back
        </button>
        <div className="artifact-detail-title">
          <h2>{filename}</h2>
          <span className="artifact-detail-meta">
            {codebase} &middot; {data.type} &middot; v{data.version}
          </span>
        </div>
        <div className="artifact-detail-toggle">
          {hasGraph && (
            <button
              className={`btn ${activeView === 'graph' ? '' : 'btn-secondary'}`}
              onClick={() => setActiveView('graph')}
            >
              Graph
            </button>
          )}
          {hasBothViews && (
            <button
              className={`btn ${activeView === 'structured' ? '' : 'btn-secondary'}`}
              onClick={() => setActiveView('structured')}
            >
              View
            </button>
          )}
          {!hasGraph && hasStructured && (
            <button
              className={`btn ${activeView === 'structured' ? '' : 'btn-secondary'}`}
              onClick={() => setActiveView('structured')}
            >
              View
            </button>
          )}
          <button
            className={`btn ${activeView === 'json' || !hasRichView ? '' : 'btn-secondary'}`}
            onClick={() => setActiveView('json')}
          >
            JSON
          </button>
        </div>
      </div>

      {/* Summary stat cards */}
      {data.summary && (
        <div className="artifact-detail-summary">
          {Object.entries(data.summary).map(([key, value]) => (
            <div key={key} className="stat">
              <div className="stat-value">{formatSummaryValue(value)}</div>
              <div className="stat-label">{key}</div>
            </div>
          ))}
        </div>
      )}

      {/* Graph, Structured, or JSON view */}
      {activeView === 'json' || !hasRichView ? (
        <div className="panel">
          <div className="panel-body">
            <pre className="artifact-json">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        </div>
      ) : activeView === 'graph' && hasGraph ? (
        <ArtifactGraph data={data} />
      ) : (
        <ArtifactStructuredView data={data} />
      )}
    </div>
  )
}
