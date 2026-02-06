import { useMemo } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  type Node,
  type Edge,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import type { ArtifactData } from '../types'

const LAYER_COLORS: Record<string, string> = {
  frontend: '#3b82f6',
  api: '#4ade80',
  database: '#fb923c',
  infrastructure: '#a78bfa',
  external: '#f87171',
  default: '#888',
}

const ENTITY_COLORS: Record<string, string> = {
  users: '#3b82f6',
  products: '#4ade80',
  orders: '#fb923c',
  payments: '#a78bfa',
  default: '#888',
}

interface ArtifactGraphProps {
  data: ArtifactData
}

export function ArtifactGraph({ data }: ArtifactGraphProps) {
  const { nodes, edges } = useMemo(() => {
    switch (data.type) {
      case 'architecture':
        return buildArchitectureGraph(data)
      case 'data-contracts':
        return buildContractsGraph(data)
      case 'product-discovery':
        return buildDiscoveryGraph(data)
      default:
        return { nodes: [], edges: [] }
    }
  }, [data])

  if (nodes.length === 0) {
    return (
      <div className="panel">
        <div className="panel-body">
          <div className="empty">
            <div className="empty-icon">{'\uD83D\uDCC9'}</div>
            <div className="empty-title">No graph data</div>
            <div>This artifact does not contain nodes or entities to visualize.</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="graph-container">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        colorMode="dark"
        proOptions={{ hideAttribution: true }}
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  )
}

function buildArchitectureGraph(data: ArtifactData): { nodes: Node[]; edges: Edge[] } {
  const archNodes = (data as Record<string, unknown>).nodes as Array<{
    id: string; label: string; type: string; layer: string; description: string; techStack?: string[]
  }> | undefined

  const archEdges = (data as Record<string, unknown>).edges as Array<{
    id: string; source: string; target: string; label: string; type: string
  }> | undefined

  if (!archNodes?.length) return { nodes: [], edges: [] }

  // Group by layer for positioning
  const layers = [...new Set(archNodes.map(n => n.layer || 'default'))]
  const layerIndex: Record<string, number> = {}
  layers.forEach((l, i) => { layerIndex[l] = i })

  const nodesPerLayer: Record<string, number> = {}

  const nodes: Node[] = archNodes.map(n => {
    const layer = n.layer || 'default'
    const layerY = (layerIndex[layer] ?? 0) * 180
    const count = nodesPerLayer[layer] || 0
    nodesPerLayer[layer] = count + 1
    const color = LAYER_COLORS[layer] || LAYER_COLORS.default

    return {
      id: n.id,
      position: { x: count * 250 + 50, y: layerY + 50 },
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontWeight: 600, color }}>{n.label}</div>
            <div style={{ fontSize: 10, color: '#888', marginTop: 2 }}>{n.type}</div>
            {n.techStack && (
              <div style={{ fontSize: 9, color: '#666', marginTop: 4 }}>
                {n.techStack.join(', ')}
              </div>
            )}
          </div>
        ),
      },
      style: {
        border: `2px solid ${color}`,
        borderRadius: 12,
        padding: 12,
        background: '#1a1a2e',
        minWidth: 160,
      },
    }
  })

  const edges: Edge[] = (archEdges || []).map(e => ({
    id: e.id,
    source: e.source,
    target: e.target,
    label: e.label,
    animated: e.type === 'async',
    style: { stroke: '#666' },
    labelStyle: { fill: '#888', fontSize: 10 },
  }))

  return { nodes, edges }
}

function buildContractsGraph(data: ArtifactData): { nodes: Node[]; edges: Edge[] } {
  const entities = (data as Record<string, unknown>).entities as Array<{
    id: string; name: string; domain: string; fields: Array<{ name: string; type: string; required?: boolean }>
  }> | undefined

  const relationships = (data as Record<string, unknown>).relationships as Array<{
    id: string; source: string; target: string; type: string; label: string
  }> | undefined

  if (!entities?.length) return { nodes: [], edges: [] }

  // Group by domain
  const domains = [...new Set(entities.map(e => e.domain || 'default'))]
  const domainIndex: Record<string, number> = {}
  domains.forEach((d, i) => { domainIndex[d] = i })

  const nodesPerDomain: Record<string, number> = {}

  const nodes: Node[] = entities.map(e => {
    const domain = e.domain || 'default'
    const domainY = (domainIndex[domain] ?? 0) * 220
    const count = nodesPerDomain[domain] || 0
    nodesPerDomain[domain] = count + 1
    const color = ENTITY_COLORS[domain] || ENTITY_COLORS.default

    return {
      id: e.id,
      position: { x: count * 280 + 50, y: domainY + 50 },
      data: {
        label: (
          <div>
            <div style={{ fontWeight: 700, color, fontSize: 14, marginBottom: 6, borderBottom: `1px solid ${color}40`, paddingBottom: 4 }}>
              {e.name}
            </div>
            {e.fields.slice(0, 6).map(f => (
              <div key={f.name} style={{ fontSize: 10, color: '#aaa', display: 'flex', gap: 6 }}>
                <span style={{ color: f.required ? '#4ade80' : '#666' }}>{f.required ? '\u25CF' : '\u25CB'}</span>
                <span>{f.name}</span>
                <span style={{ color: '#666', marginLeft: 'auto' }}>{f.type}</span>
              </div>
            ))}
            {e.fields.length > 6 && (
              <div style={{ fontSize: 9, color: '#666', marginTop: 4 }}>+{e.fields.length - 6} more</div>
            )}
          </div>
        ),
      },
      style: {
        border: `2px solid ${color}`,
        borderRadius: 8,
        padding: 10,
        background: '#1a1a2e',
        minWidth: 180,
      },
    }
  })

  const edges: Edge[] = (relationships || []).map(r => ({
    id: r.id,
    source: r.source,
    target: r.target,
    label: `${r.label} (${r.type})`,
    style: { stroke: '#666' },
    labelStyle: { fill: '#888', fontSize: 10 },
  }))

  return { nodes, edges }
}

function buildDiscoveryGraph(data: ArtifactData): { nodes: Node[]; edges: Edge[] } {
  const personas = (data as Record<string, unknown>).personas as Array<{
    id: string; name: string; role: string; isPrimary?: boolean
  }> | undefined

  const journeys = (data as Record<string, unknown>).journeys as Array<{
    id: string; name: string; persona: string; steps: Array<{ id: string; action: string; emotion: string }>
  }> | undefined

  const painPoints = (data as Record<string, unknown>).painPoints as Array<{
    id: string; description: string; severity: string; affectedPersonas: string[]
  }> | undefined

  if (!personas?.length) return { nodes: [], edges: [] }

  const nodes: Node[] = []
  const edges: Edge[] = []

  // Persona nodes
  personas.forEach((p, i) => {
    nodes.push({
      id: p.id,
      position: { x: i * 300 + 50, y: 50 },
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 24 }}>{'\uD83D\uDC64'}</div>
            <div style={{ fontWeight: 600, color: p.isPrimary ? '#4ade80' : '#e0e0e0' }}>{p.name}</div>
            <div style={{ fontSize: 10, color: '#888' }}>{p.role}</div>
          </div>
        ),
      },
      style: {
        border: `2px solid ${p.isPrimary ? '#4ade80' : '#666'}`,
        borderRadius: 50,
        padding: 16,
        background: '#1a1a2e',
        minWidth: 140,
      },
    })
  })

  // Pain point nodes
  painPoints?.forEach((pp, i) => {
    const color = pp.severity === 'critical' ? '#f87171' : pp.severity === 'high' ? '#fb923c' : '#888'
    nodes.push({
      id: pp.id,
      position: { x: i * 250 + 100, y: 250 },
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontWeight: 500, color, fontSize: 12 }}>{pp.description}</div>
            <div style={{ fontSize: 10, color: '#666', marginTop: 4 }}>{pp.severity}</div>
          </div>
        ),
      },
      style: {
        border: `1px solid ${color}`,
        borderRadius: 8,
        padding: 10,
        background: '#1a1a2e',
        maxWidth: 200,
      },
    })

    // Connect to affected personas
    pp.affectedPersonas.forEach(personaId => {
      edges.push({
        id: `${pp.id}-${personaId}`,
        source: personaId,
        target: pp.id,
        style: { stroke: color, strokeDasharray: '4 4' },
      })
    })
  })

  // Journey nodes (simplified - show as connected steps)
  journeys?.forEach((j, ji) => {
    j.steps.forEach((step, si) => {
      const nodeId = `${j.id}-${step.id}`
      nodes.push({
        id: nodeId,
        position: { x: si * 200 + 50, y: 450 + ji * 120 },
        data: {
          label: (
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 11, fontWeight: 500 }}>{step.action}</div>
              <div style={{ fontSize: 10, color: step.emotion === 'frustrated' ? '#f87171' : step.emotion === 'excited' ? '#4ade80' : '#888' }}>
                {step.emotion}
              </div>
            </div>
          ),
        },
        style: {
          border: '1px solid #444',
          borderRadius: 8,
          padding: 8,
          background: '#1a1a2e',
          minWidth: 120,
        },
      })

      // Connect steps sequentially
      if (si > 0) {
        const prevId = `${j.id}-${j.steps[si - 1].id}`
        edges.push({
          id: `${prevId}-${nodeId}`,
          source: prevId,
          target: nodeId,
          style: { stroke: '#444' },
          animated: true,
        })
      }
    })

    // Connect persona to journey start
    if (j.steps.length > 0) {
      const firstStepId = `${j.id}-${j.steps[0].id}`
      edges.push({
        id: `${j.persona}-${j.id}`,
        source: j.persona,
        target: firstStepId,
        label: j.name,
        style: { stroke: '#3b82f6' },
        labelStyle: { fill: '#3b82f6', fontSize: 10 },
      })
    }
  })

  return { nodes, edges }
}
