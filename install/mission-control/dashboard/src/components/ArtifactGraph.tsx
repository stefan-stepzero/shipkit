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

const PROVIDER_COLORS: Record<string, string> = {
  OpenAI: '#10a37f',
  Anthropic: '#d4a574',
  Gemini: '#4285f4',
  LangChain: '#1c3c3c',
  'Vercel AI': '#000',
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
      case 'prompt-audit':
        return buildPromptAuditGraph(data)
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

function buildPromptAuditGraph(data: ArtifactData): { nodes: Node[]; edges: Edge[] } {
  const pipelines = (data as Record<string, unknown>).pipelines as Array<{
    id: string; name: string; type: string
    stages: Array<{ id: string; promptId: string; provider: string; purpose: string; location: string }>
    edges: Array<{ id: string; source: string; target: string; dataFlow: string; validated: boolean }>
    issues?: string[]
  }> | undefined

  const prompts = (data as Record<string, unknown>).prompts as Array<{
    id: string; location: string; provider: string; purpose: string; pipelineType: string; score: number
    issues: Array<{ id: string; severity: string }>
  }> | undefined

  if (!pipelines?.length && !prompts?.length) return { nodes: [], edges: [] }

  const nodes: Node[] = []
  const edges: Edge[] = []

  // Collect prompt IDs referenced by pipeline stages
  const pipelinePromptIds = new Set<string>()
  pipelines?.forEach(p => p.stages.forEach(s => pipelinePromptIds.add(s.promptId)))

  // Render each pipeline as connected stages
  let pipelineOffsetY = 0
  pipelines?.forEach((pipeline) => {
    const hasIssues = pipeline.issues && pipeline.issues.length > 0
    const pipelineColor = hasIssues ? '#fb923c' : '#4ade80'

    // Pipeline label node
    nodes.push({
      id: `${pipeline.id}-label`,
      position: { x: 0, y: pipelineOffsetY },
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontWeight: 700, color: pipelineColor, fontSize: 13 }}>{pipeline.name}</div>
            <div style={{ fontSize: 10, color: '#888', marginTop: 2 }}>{pipeline.type} pipeline</div>
          </div>
        ),
      },
      style: {
        border: `1px dashed ${pipelineColor}60`,
        borderRadius: 8,
        padding: 10,
        background: `${pipelineColor}08`,
        minWidth: 180,
      },
      selectable: false,
      draggable: true,
    })

    // Stage nodes
    const stageY = pipelineOffsetY + 80
    pipeline.stages.forEach((stage, si) => {
      const providerColor = PROVIDER_COLORS[stage.provider] || PROVIDER_COLORS.default
      const scoreInfo = getPromptScore(prompts, stage.promptId)

      nodes.push({
        id: stage.id,
        position: { x: si * 240 + 40, y: stageY },
        data: {
          label: (
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontWeight: 600, color: providerColor, fontSize: 12 }}>{stage.purpose}</div>
              <div style={{ fontSize: 10, color: '#888', marginTop: 4 }}>{stage.provider}</div>
              <div style={{ fontSize: 9, color: '#666', marginTop: 2, fontFamily: 'monospace' }}>{stage.location}</div>
              {scoreInfo && (
                <div style={{ fontSize: 10, color: scoreInfo.color, marginTop: 4, fontWeight: 600 }}>
                  score: {scoreInfo.score}
                </div>
              )}
            </div>
          ),
        },
        style: {
          border: `2px solid ${providerColor}`,
          borderRadius: 12,
          padding: 12,
          background: '#1a1a2e',
          minWidth: 180,
        },
      })
    })

    // Data flow edges — green if validated, red+animated if not
    pipeline.edges.forEach(e => {
      const edgeColor = e.validated ? '#4ade80' : '#f87171'
      edges.push({
        id: e.id,
        source: e.source,
        target: e.target,
        label: `${e.dataFlow}${e.validated ? ' \u2713' : ' \u26A0'}`,
        animated: !e.validated,
        style: { stroke: edgeColor },
        labelStyle: { fill: edgeColor, fontSize: 10 },
      })
    })

    // Dashed connector from pipeline label to first stage
    if (pipeline.stages.length > 0) {
      edges.push({
        id: `${pipeline.id}-start`,
        source: `${pipeline.id}-label`,
        target: pipeline.stages[0].id,
        style: { stroke: '#444', strokeDasharray: '4 4' },
      })
    }

    pipelineOffsetY += 240
  })

  // Standalone single-stage prompts not part of any pipeline
  const standalonePrompts = prompts?.filter(p => p.pipelineType === 'single' && !pipelinePromptIds.has(p.id)) || []
  if (standalonePrompts.length > 0) {
    nodes.push({
      id: 'standalone-label',
      position: { x: 0, y: pipelineOffsetY },
      data: {
        label: (
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontWeight: 700, color: '#888', fontSize: 13 }}>Standalone Prompts</div>
            <div style={{ fontSize: 10, color: '#666', marginTop: 2 }}>{standalonePrompts.length} single-stage</div>
          </div>
        ),
      },
      style: {
        border: '1px dashed #44444460',
        borderRadius: 8,
        padding: 10,
        background: '#88880808',
        minWidth: 180,
      },
      selectable: false,
      draggable: true,
    })

    standalonePrompts.forEach((prompt, pi) => {
      const providerColor = PROVIDER_COLORS[prompt.provider] || PROVIDER_COLORS.default
      const hasCritical = prompt.issues.some(i => i.severity === 'critical')
      const borderColor = hasCritical ? '#f87171' : providerColor

      nodes.push({
        id: `standalone-${prompt.id}`,
        position: { x: pi * 220 + 40, y: pipelineOffsetY + 80 },
        data: {
          label: (
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontWeight: 600, color: providerColor, fontSize: 12 }}>{prompt.purpose}</div>
              <div style={{ fontSize: 10, color: '#888', marginTop: 4 }}>{prompt.provider}</div>
              <div style={{ fontSize: 9, color: '#666', marginTop: 2, fontFamily: 'monospace' }}>{prompt.location}</div>
              <div style={{
                fontSize: 10, marginTop: 4, fontWeight: 600,
                color: prompt.score >= 8 ? '#4ade80' : prompt.score >= 5 ? '#fb923c' : '#f87171',
              }}>
                score: {prompt.score}
              </div>
              {prompt.issues.length > 0 && (
                <div style={{ fontSize: 9, color: '#f87171', marginTop: 2 }}>
                  {prompt.issues.length} issue{prompt.issues.length > 1 ? 's' : ''}
                </div>
              )}
            </div>
          ),
        },
        style: {
          border: `2px solid ${borderColor}`,
          borderRadius: 12,
          padding: 12,
          background: '#1a1a2e',
          minWidth: 160,
        },
      })
    })
  }

  return { nodes, edges }
}

/** Look up a prompt's score by ID for coloring stage nodes */
function getPromptScore(
  prompts: Array<{ id: string; score: number }> | undefined,
  promptId: string
): { score: number; color: string } | null {
  const prompt = prompts?.find(p => p.id === promptId)
  if (!prompt) return null
  const color = prompt.score >= 8 ? '#4ade80' : prompt.score >= 5 ? '#fb923c' : '#f87171'
  return { score: prompt.score, color }
}
