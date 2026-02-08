export interface Instance {
  sessionId: string
  project: string
  projectPath: string
  firstSeen: number
  lastSeen: number
  lastEvent: string
  lastTool: string
  toolCount: number
  skills: string[]
  status: 'active' | 'stale' | 'stopped'
  mode?: 'standby' | null
}

export interface QueueItem {
  commandId: string
  status: 'pending' | 'inflight' | 'processed'
  prompt: string
  source: string
  timestamp: number
}

export interface QueueStatus {
  sessionId: string
  pending: QueueItem[]
  inflight: QueueItem[]
  processed: QueueItem[]
  total: number
}

export interface Event {
  sessionId: string
  project: string
  projectPath: string
  event: string
  tool: string
  skill?: string
  timestamp: number
  receivedAt: number
}

export interface Stats {
  totalInstances: number
  activeInstances: number
  totalCodebases: number
  totalEvents: number
  uptime: number
}

export interface Recommendation {
  type: string
  skill: string
  message: string
  priority: 'high' | 'medium' | 'low'
  action: string
  source: string
}

export interface QuickAction {
  skill: string
  label: string
  icon: string
}

export interface SkillUsage {
  name: string
  firstUsed: number
  lastUsed: number
  useCount: number
}

export interface Codebase {
  projectPath: string
  projectName: string
  firstSeen: number
  lastActivity: number
  skills: Record<string, SkillUsage>
  totalSkillUses: number
  recommendations: Recommendation[]
  quickActions: QuickAction[]
  skillCount: number
  artifacts?: Record<string, ArtifactData>
}

export interface ArtifactData {
  $schema: string
  type: string
  version: string
  lastUpdated: string
  source: string
  summary: Record<string, unknown>
  [key: string]: unknown
}

// Architecture artifact graph types (for React Flow)
export interface ArchitectureNode {
  id: string
  label: string
  type: string
  layer: string
  description: string
  techStack?: string[]
  status?: string
}

export interface ArchitectureEdge {
  id: string
  source: string
  target: string
  label: string
  type: string
  protocol?: string
}

export interface ArchitectureArtifact extends ArtifactData {
  type: 'architecture'
  nodes: ArchitectureNode[]
  edges: ArchitectureEdge[]
  decisions: Array<{
    id: string
    title: string
    date: string
    status: string
    chosen: string
    alternatives: string[]
    rationale: string
  }>
}

// Contracts artifact types (for ER diagrams)
export interface ContractsArtifact extends ArtifactData {
  type: 'data-contracts'
  entities: Array<{
    id: string
    name: string
    domain: string
    fields: Array<{ name: string; type: string; required?: boolean }>
  }>
  relationships: Array<{
    id: string
    source: string
    target: string
    type: string
    label: string
  }>
}

// Routing
export type AppRoute =
  | { view: 'portfolio' }
  | { view: 'project'; projectPath: string }

// Foundation artifacts — project-wide, most other skills depend on these
export const FOUNDATIONAL_ARTIFACTS = ['project-why', 'stack', 'codebase-index', 'goals', 'architecture'] as const

// Per-feature artifacts — many of these exist, state (active/done) matters
export const PER_FEATURE_ARTIFACTS = ['spec', 'plan', 'bug-spec'] as const

// Quality gate artifacts — run periodically, freshness matters
export const QUALITY_ARTIFACTS = ['preflight', 'scale-readiness', 'prompt-audit', 'ux-decisions', 'test-coverage'] as const

// All known artifact types
export const ALL_ARTIFACT_TYPES = [
  // Foundation
  'project-why', 'stack', 'codebase-index', 'goals', 'architecture',
  // Per-feature
  'spec', 'plan', 'bug-spec',
  // Quality gates
  'preflight', 'scale-readiness', 'prompt-audit', 'ux-decisions', 'test-coverage',
  // Context & progress
  'project-status', 'data-contracts', 'product-discovery', 'work-memory', 'user-tasks',
] as const

export type ArtifactType = typeof ALL_ARTIFACT_TYPES[number]

export const ARTIFACT_TYPE_ICONS: Record<string, string> = {
  // Foundation
  'project-why': '\uD83E\uDD14',
  stack: '\uD83D\uDEE0\uFE0F',
  'codebase-index': '\uD83D\uDCC2',
  goals: '\uD83C\uDFAF',
  architecture: '\uD83C\uDFD7\uFE0F',
  // Per-feature
  spec: '\uD83D\uDCC4',
  plan: '\uD83D\uDCCB',
  'bug-spec': '\uD83D\uDC1B',
  // Quality gates
  preflight: '\uD83D\uDE80',
  'scale-readiness': '\uD83D\uDCC8',
  'prompt-audit': '\uD83D\uDD0D',
  'ux-decisions': '\uD83C\uDFA8',
  'test-coverage': '\uD83E\uDDEA',
  // Context & progress
  'project-status': '\uD83D\uDCCA',
  'data-contracts': '\uD83D\uDD17',
  'product-discovery': '\uD83D\uDC65',
  'work-memory': '\uD83D\uDCDD',
  'user-tasks': '\u2705',
}
