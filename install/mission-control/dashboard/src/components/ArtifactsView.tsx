import { useState } from 'react'
import type { Codebase, ArtifactData } from '../types'
import { ArtifactGraph } from './ArtifactGraph'

const ARTIFACT_ICONS: Record<string, string> = {
  goals: '\uD83C\uDFAF',
  status: '\uD83D\uDCCA',
  architecture: '\uD83C\uDFD7\uFE0F',
  'data-contracts': '\uD83D\uDD17',
  'product-discovery': '\uD83D\uDC65',
  'work-memory': '\uD83D\uDCDD',
  'codebase-index': '\uD83D\uDCC2',
  stack: '\uD83E\uDDF1',
  preflight: '\uD83D\uDE80',
  'scale-readiness': '\uD83D\uDCC8',
  'prompt-audit': '\uD83D\uDD0D',
  'user-tasks': '\u2705',
  coverage: '\uD83E\uDDEA',
}

// Artifacts that have graph visualization support
const GRAPH_ARTIFACTS = new Set(['architecture', 'data-contracts', 'product-discovery'])

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
      <div className="container-full">
        <div className="panel">
          <div className="panel-header">
            <h2>Artifacts</h2>
          </div>
          <div className="panel-body">
            <div className="empty">
              <div className="empty-icon">{'\uD83D\uDCE6'}</div>
              <div className="empty-title">No artifacts received yet</div>
              <div>
                Run Shipkit skills in a project to generate .shipkit/*.json artifacts.
                <br />
                The reporter hook will automatically send them here.
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container-full">
      {selectedArtifact ? (
        <ArtifactDetail
          codebase={selectedArtifact.codebase}
          filename={selectedArtifact.filename}
          data={selectedArtifact.data}
          onBack={() => setSelectedArtifact(null)}
        />
      ) : (
        codebasesWithArtifacts.map(cb => (
          <div key={cb.projectPath} style={{ marginBottom: 24 }}>
            <h2 style={{ fontSize: 18, marginBottom: 12, color: 'var(--text)' }}>
              {cb.projectName}
              <span style={{ fontSize: 12, color: 'var(--text-dim)', marginLeft: 12, fontWeight: 'normal' }}>
                {cb.projectPath}
              </span>
            </h2>
            <div className="artifact-grid">
              {Object.entries(cb.artifacts!).map(([filename, data]) => (
                <ArtifactCard
                  key={filename}
                  filename={filename}
                  data={data}
                  hasGraph={GRAPH_ARTIFACTS.has(data.type)}
                  onClick={() => setSelectedArtifact({
                    codebase: cb.projectName,
                    filename,
                    data,
                  })}
                />
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  )
}

function ArtifactCard({
  filename,
  data,
  hasGraph,
  onClick,
}: {
  filename: string
  data: ArtifactData
  hasGraph: boolean
  onClick: () => void
}) {
  const icon = ARTIFACT_ICONS[data.type] || '\uD83D\uDCC4'
  const summary = data.summary || {}
  const summaryEntries = Object.entries(summary).slice(0, 3)

  return (
    <div className="artifact-card" onClick={onClick}>
      <div className="artifact-card-header">
        <span style={{ fontSize: 24 }}>{icon}</span>
        <div style={{ display: 'flex', gap: 6 }}>
          <span className="artifact-card-type">{data.type}</span>
          {hasGraph && (
            <span className="artifact-card-type" style={{ background: 'rgba(74, 222, 128, 0.2)', color: 'var(--accent-green)' }}>
              graph
            </span>
          )}
        </div>
      </div>
      <h3>{filename}</h3>
      <div className="artifact-card-summary">
        {summaryEntries.map(([key, value]) => (
          <div key={key}>
            <span style={{ color: 'var(--text-dim)' }}>{key}:</span>{' '}
            {String(value)}
          </div>
        ))}
      </div>
      <div className="artifact-card-meta">
        <span>v{data.version}</span>
        <span>{data.lastUpdated}</span>
        <span>via {data.source}</span>
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
  const [showJson, setShowJson] = useState(false)
  const hasGraph = GRAPH_ARTIFACTS.has(data.type)

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16 }}>
        <button className="btn btn-secondary" onClick={onBack}>
          {'\u2190'} Back
        </button>
        <div>
          <h2 style={{ fontSize: 20 }}>{filename}</h2>
          <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
            {codebase} &middot; {data.type} &middot; v{data.version}
          </span>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
          {hasGraph && (
            <button
              className={`btn ${showJson ? 'btn-secondary' : ''}`}
              onClick={() => setShowJson(false)}
            >
              Graph
            </button>
          )}
          <button
            className={`btn ${showJson || !hasGraph ? '' : 'btn-secondary'}`}
            onClick={() => setShowJson(true)}
          >
            JSON
          </button>
        </div>
      </div>

      {/* Summary cards */}
      {data.summary && (
        <div style={{ display: 'flex', gap: 16, marginBottom: 24, flexWrap: 'wrap' }}>
          {Object.entries(data.summary).map(([key, value]) => (
            <div key={key} className="stat">
              <div className="stat-value" style={{ fontSize: 20 }}>
                {String(value)}
              </div>
              <div className="stat-label">{key}</div>
            </div>
          ))}
        </div>
      )}

      {/* Graph or JSON view */}
      {showJson || !hasGraph ? (
        <div className="panel">
          <div className="panel-body">
            <pre style={{
              background: 'var(--bg-card)',
              padding: 16,
              borderRadius: 8,
              overflow: 'auto',
              maxHeight: 600,
              fontSize: 13,
              lineHeight: 1.5,
              color: 'var(--accent-green)',
            }}>
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        </div>
      ) : (
        <ArtifactGraph data={data} />
      )}
    </div>
  )
}
