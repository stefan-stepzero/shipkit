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
