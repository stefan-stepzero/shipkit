import { useState, useEffect, useCallback } from 'react'
import type { Stats, Instance, Event, Codebase } from '../types'
import { fetchStats, fetchInstances, fetchEvents, fetchCodebases } from '../api'

interface DashboardData {
  stats: Stats | null
  instances: Instance[]
  events: Event[]
  codebases: Codebase[]
  loading: boolean
  error: string | null
}

export function useDashboardData(refreshInterval = 3000): DashboardData {
  const [stats, setStats] = useState<Stats | null>(null)
  const [instances, setInstances] = useState<Instance[]>([])
  const [events, setEvents] = useState<Event[]>([])
  const [codebases, setCodebases] = useState<Codebase[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    try {
      const [s, i, e, c] = await Promise.all([
        fetchStats(),
        fetchInstances(),
        fetchEvents(),
        fetchCodebases(),
      ])
      setStats(s)
      setInstances(i)
      setEvents(e)
      setCodebases(c)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to Mission Control server')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refresh()
    const interval = setInterval(refresh, refreshInterval)
    return () => clearInterval(interval)
  }, [refresh, refreshInterval])

  return { stats, instances, events, codebases, loading, error }
}
