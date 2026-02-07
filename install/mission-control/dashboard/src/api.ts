import type { Stats, Instance, Event, Codebase, QueueStatus } from './types'

const BASE = ''

export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${BASE}/api/stats`)
  return res.json()
}

export async function fetchInstances(): Promise<Instance[]> {
  const res = await fetch(`${BASE}/api/instances`)
  const data = await res.json()
  return data.instances
}

export async function fetchEvents(limit = 50): Promise<Event[]> {
  const res = await fetch(`${BASE}/api/events?limit=${limit}`)
  const data = await res.json()
  return data.events
}

export async function fetchCodebases(): Promise<Codebase[]> {
  const res = await fetch(`${BASE}/api/codebases`)
  const data = await res.json()
  return data.codebases
}

export async function fetchCodebase(projectPath: string): Promise<Codebase> {
  const res = await fetch(`${BASE}/api/codebases/${encodeURIComponent(projectPath)}`)
  return res.json()
}

export async function fetchQueue(sessionId: string): Promise<QueueStatus> {
  const res = await fetch(`${BASE}/api/queue/${encodeURIComponent(sessionId)}`)
  return res.json()
}

export interface SendCommandResult {
  queued: boolean
  sessionId: string
  commandId: string
}

export async function sendCommand(sessionId: string, prompt: string, source = 'Mission Control Dashboard'): Promise<SendCommandResult> {
  const res = await fetch(`${BASE}/api/command`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId, prompt, source }),
  })
  return res.json()
}

export async function fetchEventsForProject(projectPath: string, limit = 100): Promise<Event[]> {
  // The server doesn't have a project filter yet, so fetch all and filter client-side
  const res = await fetch(`${BASE}/api/events?limit=${limit}`)
  const data = await res.json()
  return (data.events as Event[]).filter(e => e.projectPath === projectPath)
}
