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

// Foundational artifact types for coverage display
export const FOUNDATIONAL_ARTIFACTS = ['goals', 'spec', 'plan', 'preflight', 'architecture'] as const

// All known artifact types
export const ALL_ARTIFACT_TYPES = [
  'goals', 'project-status', 'architecture', 'data-contracts', 'product-discovery',
  'work-memory', 'codebase-index', 'preflight', 'scale-readiness', 'prompt-audit',
  'user-tasks', 'test-coverage', 'spec', 'plan', 'bug-spec', 'ux-decisions', 'project-why'
] as const

export type ArtifactType = typeof ALL_ARTIFACT_TYPES[number]

export const ARTIFACT_TYPE_ICONS: Record<string, string> = {
  goals: '\uD83C\uDFAF',
  'project-status': '\uD83D\uDCCA',
  architecture: '\uD83C\uDFD7\uFE0F',
  'data-contracts': '\uD83D\uDD17',
  'product-discovery': '\uD83D\uDC65',
  'work-memory': '\uD83D\uDCDD',
  'codebase-index': '\uD83D\uDCC2',
  preflight: '\uD83D\uDE80',
  'scale-readiness': '\uD83D\uDCC8',
  'prompt-audit': '\uD83D\uDD0D',
  'user-tasks': '\u2705',
  'test-coverage': '\uD83E\uDDEA',
  spec: '\uD83D\uDCC4',
  plan: '\uD83D\uDCCB',
  'bug-spec': '\uD83D\uDC1B',
  'ux-decisions': '\uD83C\uDFA8',
  'project-why': '\uD83E\uDD14',
}
