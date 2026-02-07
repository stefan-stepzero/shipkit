import type { ArtifactData } from '../types'

interface RendererProps {
  data: ArtifactData
}

export function ArtifactStructuredView({ data }: RendererProps) {
  switch (data.type) {
    case 'goals': return <GoalsRenderer data={data} />
    case 'preflight': return <PreflightRenderer data={data} />
    case 'project-status': return <ProjectStatusRenderer data={data} />
    case 'plan': return <PlanRenderer data={data} />
    case 'spec': return <SpecRenderer data={data} />
    case 'test-coverage': return <TestCoverageRenderer data={data} />
    case 'work-memory': return <WorkMemoryRenderer data={data} />
    case 'scale-readiness': return <ScaleReadyRenderer data={data} />
    case 'bug-spec': return <BugSpecRenderer data={data} />
    case 'prompt-audit': return <PromptAuditRenderer data={data} />
    case 'ux-decisions': return <UxDecisionsRenderer data={data} />
    case 'user-tasks': return <UserTasksRenderer data={data} />
    case 'project-why': return <ProjectWhyRenderer data={data} />
    case 'codebase-index': return <CodebaseIndexRenderer data={data} />
    default: return <FallbackRenderer data={data} />
  }
}

// ─── Helpers ─────────────────────────────────────────

function StatusBadge({ status, map }: { status: string; map?: Record<string, string> }) {
  const defaultMap: Record<string, string> = {
    pass: 'var(--accent-green)',
    achieved: 'var(--accent-green)',
    complete: 'var(--accent-green)',
    verified: 'var(--accent-green)',
    'in-progress': 'var(--accent-blue)',
    active: 'var(--accent-blue)',
    pending: 'var(--accent-orange)',
    'not-started': 'var(--text-muted)',
    warning: 'var(--accent-orange)',
    fail: 'var(--accent-red)',
    stale: 'var(--accent-orange)',
    deferred: 'var(--text-dim)',
    orphaned: 'var(--accent-red)',
    'needs-work': 'var(--accent-orange)',
    ready: 'var(--accent-green)',
    'ready-with-warnings': 'var(--accent-orange)',
    'not-ready': 'var(--accent-red)',
    'human-verify': '#a78bfa',
    na: 'var(--text-dim)',
    'not-applicable': 'var(--text-dim)',
    missing: 'var(--accent-red)',
    fresh: 'var(--accent-green)',
    aging: 'var(--accent-orange)',
  }
  const colorMap = map || defaultMap
  const color = colorMap[status] || 'var(--text-muted)'
  return (
    <span className="ar-badge" style={{ background: `${color}22`, color, borderColor: `${color}44` }}>
      {status}
    </span>
  )
}

function ProgressBar({ value, max = 100, color }: { value: number; max?: number; color?: string }) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  const barColor = color || (pct >= 80 ? 'var(--accent-green)' : pct >= 50 ? 'var(--accent-orange)' : 'var(--accent-red)')
  return (
    <div className="ar-progress">
      <div className="ar-progress-bar" style={{ width: `${pct}%`, background: barColor }} />
      <span className="ar-progress-label">{pct}%</span>
    </div>
  )
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="ar-section">
      <h4 className="ar-section-title">{title}</h4>
      {children}
    </div>
  )
}

// ─── Goals ───────────────────────────────────────────

function GoalsRenderer({ data }: RendererProps) {
  const goals = (data as any).goals as Array<{
    id: string; name: string; priority: string; status: string; objective: string
    successCriteria?: string[]; notes?: string | null
  }> | undefined

  if (!goals?.length) return <FallbackRenderer data={data} />

  const byPriority = (data.summary as any)?.byPriority || {}

  return (
    <div className="ar-container">
      <div className="ar-stats-row">
        {Object.entries(byPriority).map(([k, v]) => (
          <div key={k} className="ar-stat-chip">
            <span className="ar-stat-chip-value">{String(v)}</span>
            <span className="ar-stat-chip-label">{k.toUpperCase()}</span>
          </div>
        ))}
      </div>

      <Section title="Goals">
        {goals.map(g => (
          <div key={g.id} className="ar-card">
            <div className="ar-card-header">
              <span className="ar-card-title">{g.name}</span>
              <div style={{ display: 'flex', gap: 6 }}>
                <StatusBadge status={g.priority} />
                <StatusBadge status={g.status} />
              </div>
            </div>
            <div className="ar-card-body">{g.objective}</div>
            {g.successCriteria && g.successCriteria.length > 0 && (
              <div className="ar-checklist">
                {g.successCriteria.map((c, i) => (
                  <div key={i} className="ar-checklist-item">
                    <span style={{ color: g.status === 'achieved' ? 'var(--accent-green)' : 'var(--text-dim)' }}>
                      {g.status === 'achieved' ? '\u2713' : '\u25CB'}
                    </span>
                    {c}
                  </div>
                ))}
              </div>
            )}
            {g.notes && <div className="ar-card-note">{g.notes}</div>}
          </div>
        ))}
      </Section>
    </div>
  )
}

// ─── Preflight ───────────────────────────────────────

function PreflightRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const checks = (data as any).checks as Array<{
    id: string; category: string; name: string; status: string; details?: string
  }> | undefined
  const blockers = (data as any).blockers as Array<{ name: string; problem: string; fix?: string }> | undefined

  const score = summary?.readinessScore ?? 0
  const counts = summary?.counts || {}

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <div className="ar-hero-score" style={{ color: score >= 80 ? 'var(--accent-green)' : score >= 50 ? 'var(--accent-orange)' : 'var(--accent-red)' }}>
          {score}
        </div>
        <div className="ar-hero-label">Readiness Score</div>
        <StatusBadge status={summary?.overallStatus || 'unknown'} />
      </div>

      <div className="ar-stats-row">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} className="ar-stat-chip">
            <span className="ar-stat-chip-value">{String(v)}</span>
            <span className="ar-stat-chip-label">{k}</span>
          </div>
        ))}
      </div>

      {blockers && blockers.length > 0 && (
        <Section title={`Blockers (${blockers.length})`}>
          {blockers.map((b, i) => (
            <div key={i} className="ar-card" style={{ borderLeftColor: 'var(--accent-red)' }}>
              <div className="ar-card-header"><span className="ar-card-title">{b.name}</span></div>
              <div className="ar-card-body">{b.problem}</div>
              {b.fix && <div className="ar-card-note" style={{ color: 'var(--accent-green)' }}>Fix: {b.fix}</div>}
            </div>
          ))}
        </Section>
      )}

      {checks && (
        <Section title="Checks">
          <div className="ar-check-grid">
            {checks.map(c => (
              <div key={c.id} className="ar-check-item">
                <span className="ar-check-icon" style={{
                  color: c.status === 'pass' ? 'var(--accent-green)' : c.status === 'fail' ? 'var(--accent-red)' : c.status === 'warning' ? 'var(--accent-orange)' : 'var(--text-dim)'
                }}>
                  {c.status === 'pass' ? '\u2713' : c.status === 'fail' ? '\u2717' : c.status === 'warning' ? '\u26A0' : '\u2014'}
                </span>
                <span>{c.name}</span>
              </div>
            ))}
          </div>
        </Section>
      )}
    </div>
  )
}

// ─── Project Status ──────────────────────────────────

function ProjectStatusRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const gaps = (data as any).gaps as Array<{
    id: string; severity: string; description: string; suggestedAction?: string
  }> | undefined
  const workflow = (data as any).workflow as any
  const recs = (data as any).recommendations as Array<{ priority: number; action: string; reason: string }> | undefined

  const healthScore = summary?.healthScore ?? 0

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <div className="ar-hero-score" style={{ color: healthScore >= 80 ? 'var(--accent-green)' : healthScore >= 50 ? 'var(--accent-orange)' : 'var(--accent-red)' }}>
          {healthScore}
        </div>
        <div className="ar-hero-label">Health Score</div>
      </div>

      {workflow && (
        <div className="ar-stats-row">
          <div className="ar-stat-chip"><span className="ar-stat-chip-value">{workflow.specs?.activeCount ?? 0}</span><span className="ar-stat-chip-label">Specs</span></div>
          <div className="ar-stat-chip"><span className="ar-stat-chip-value">{workflow.plans?.count ?? 0}</span><span className="ar-stat-chip-label">Plans</span></div>
          <div className="ar-stat-chip"><span className="ar-stat-chip-value">{workflow.tasks?.activeCount ?? 0}</span><span className="ar-stat-chip-label">Tasks</span></div>
        </div>
      )}

      {gaps && gaps.length > 0 && (
        <Section title={`Gaps (${gaps.length})`}>
          {gaps.map(g => (
            <div key={g.id} className="ar-card" style={{
              borderLeftColor: g.severity === 'critical' ? 'var(--accent-red)' : g.severity === 'warning' ? 'var(--accent-orange)' : 'var(--text-muted)'
            }}>
              <div className="ar-card-header">
                <span className="ar-card-title">{g.description}</span>
                <StatusBadge status={g.severity} />
              </div>
              {g.suggestedAction && <div className="ar-card-note" style={{ color: 'var(--accent-blue)' }}>{g.suggestedAction}</div>}
            </div>
          ))}
        </Section>
      )}

      {recs && recs.length > 0 && (
        <Section title="Recommendations">
          {recs.map((r, i) => (
            <div key={i} className="ar-card">
              <div className="ar-card-header">
                <span className="ar-card-title" style={{ color: 'var(--accent-blue)' }}>{r.action}</span>
              </div>
              <div className="ar-card-body">{r.reason}</div>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Plan ────────────────────────────────────────────

function PlanRenderer({ data }: RendererProps) {
  const plan = (data as any).plan as any
  if (!plan) return <FallbackRenderer data={data} />

  const phases = plan.phases as Array<{
    id: string; name: string; tasks: Array<{ id: string; description: string; status: string; estimatedHours?: number }>
    gate?: { condition: string }
  }> | undefined
  const planSummary = plan.summary || {}
  const decisions = plan.decisions as Array<{ decision: string; rationale: string }> | undefined
  const risks = plan.risks as Array<{ risk: string; likelihood: string; impact: string }> | undefined

  const totalTasks = planSummary.taskCount || 0
  const completion = planSummary.completionPercentage || 0

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <div className="ar-hero-score" style={{ color: 'var(--accent-blue)' }}>{plan.name || 'Plan'}</div>
        <StatusBadge status={plan.status || 'draft'} />
      </div>

      <div className="ar-stats-row">
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{planSummary.phaseCount || 0}</span><span className="ar-stat-chip-label">Phases</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{totalTasks}</span><span className="ar-stat-chip-label">Tasks</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{planSummary.filesCreated || 0}</span><span className="ar-stat-chip-label">New Files</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{planSummary.filesModified || 0}</span><span className="ar-stat-chip-label">Modified</span></div>
      </div>

      <ProgressBar value={completion} />

      {phases && (
        <Section title="Phases">
          {phases.map(phase => {
            const done = phase.tasks.filter(t => t.status === 'done' || t.status === 'complete').length
            return (
              <div key={phase.id} className="ar-card">
                <div className="ar-card-header">
                  <span className="ar-card-title">{phase.name}</span>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{done}/{phase.tasks.length} tasks</span>
                </div>
                {phase.gate && <div className="ar-card-note">Gate: {phase.gate.condition}</div>}
                <div className="ar-task-list">
                  {phase.tasks.map(t => (
                    <div key={t.id} className="ar-task-item">
                      <StatusBadge status={t.status} />
                      <span>{t.id}: {t.description}</span>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </Section>
      )}

      {decisions && decisions.length > 0 && (
        <Section title="Decisions">
          {decisions.map((d, i) => (
            <div key={i} className="ar-card">
              <div className="ar-card-header"><span className="ar-card-title">{d.decision}</span></div>
              <div className="ar-card-body">{d.rationale}</div>
            </div>
          ))}
        </Section>
      )}

      {risks && risks.length > 0 && (
        <Section title="Risks">
          {risks.map((r, i) => (
            <div key={i} className="ar-card">
              <div className="ar-card-header">
                <span className="ar-card-title">{r.risk}</span>
                <div style={{ display: 'flex', gap: 6 }}>
                  <StatusBadge status={`L:${r.likelihood}`} />
                  <StatusBadge status={`I:${r.impact}`} />
                </div>
              </div>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Spec ────────────────────────────────────────────

function SpecRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const scenarios = (data as any).scenarios as Array<{
    id: string; name: string; type: string; then: string[]
  }> | undefined
  const edgeCases = (data as any).edgeCases as Record<string, string[]> | undefined
  const ac = (data as any).acceptanceCriteria as { mustHave?: string[]; shouldHave?: string[]; wontHave?: string[] } | undefined

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <div className="ar-hero-score" style={{ color: 'var(--accent-blue)', fontSize: 24 }}>{summary?.name || 'Spec'}</div>
        <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
          <StatusBadge status={summary?.status || 'draft'} />
          <StatusBadge status={summary?.complexity || 'unknown'} />
          <StatusBadge status={summary?.featureType || 'unknown'} />
        </div>
      </div>

      <div className="ar-stats-row">
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.scenarioCount || 0}</span><span className="ar-stat-chip-label">Scenarios</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.acceptanceCriteriaCount || 0}</span><span className="ar-stat-chip-label">Criteria</span></div>
      </div>

      {scenarios && (
        <Section title="Scenarios">
          {scenarios.map(s => (
            <div key={s.id} className="ar-card">
              <div className="ar-card-header">
                <span className="ar-card-title">{s.name}</span>
                <StatusBadge status={s.type} />
              </div>
              <div className="ar-checklist">
                {s.then.map((t, i) => (
                  <div key={i} className="ar-checklist-item"><span style={{ color: 'var(--accent-green)' }}>{'\u2192'}</span> {t}</div>
                ))}
              </div>
            </div>
          ))}
        </Section>
      )}

      {edgeCases && (
        <Section title="Edge Cases">
          <div className="ar-stats-row" style={{ flexWrap: 'wrap' }}>
            {Object.entries(edgeCases).map(([cat, items]) => (
              <div key={cat} className="ar-stat-chip">
                <span className="ar-stat-chip-value">{(items as string[]).length}</span>
                <span className="ar-stat-chip-label">{cat}</span>
              </div>
            ))}
          </div>
        </Section>
      )}

      {ac && (
        <Section title="Acceptance Criteria">
          {ac.mustHave && ac.mustHave.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 12, color: 'var(--accent-green)', marginBottom: 6, textTransform: 'uppercase' }}>Must Have</div>
              <div className="ar-checklist">
                {ac.mustHave.map((c, i) => (
                  <div key={i} className="ar-checklist-item"><span style={{ color: 'var(--accent-green)' }}>{'\u25CB'}</span> {c}</div>
                ))}
              </div>
            </div>
          )}
          {ac.shouldHave && ac.shouldHave.length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <div style={{ fontSize: 12, color: 'var(--accent-blue)', marginBottom: 6, textTransform: 'uppercase' }}>Should Have</div>
              <div className="ar-checklist">
                {ac.shouldHave.map((c, i) => (
                  <div key={i} className="ar-checklist-item"><span style={{ color: 'var(--accent-blue)' }}>{'\u25CB'}</span> {c}</div>
                ))}
              </div>
            </div>
          )}
        </Section>
      )}
    </div>
  )
}

// ─── Test Coverage ───────────────────────────────────

function TestCoverageRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const cases = (data as any).cases as Array<{
    id: string; name: string; priority: string; status: string; sourceFile: string
  }> | undefined
  const gaps = (data as any).gaps as Array<{ file: string; reason: string; priority: string }> | undefined
  const staleCases = (data as any).staleCases as Array<{ caseId: string; sourceFile: string }> | undefined

  const coverageScore = summary?.coverageScore ?? 0

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <div className="ar-hero-score" style={{ color: coverageScore >= 80 ? 'var(--accent-green)' : coverageScore >= 50 ? 'var(--accent-orange)' : 'var(--accent-red)' }}>
          {coverageScore}%
        </div>
        <div className="ar-hero-label">Coverage Score</div>
      </div>

      <ProgressBar value={coverageScore} />

      <div className="ar-stats-row">
        {summary?.byStatus && Object.entries(summary.byStatus).map(([k, v]) => (
          <div key={k} className="ar-stat-chip">
            <span className="ar-stat-chip-value">{String(v)}</span>
            <span className="ar-stat-chip-label">{k}</span>
          </div>
        ))}
      </div>

      {cases && (
        <Section title={`Test Cases (${cases.length})`}>
          {cases.map(c => (
            <div key={c.id} className="ar-task-item">
              <StatusBadge status={c.status} />
              <StatusBadge status={c.priority} />
              <span style={{ flex: 1 }}>{c.id}: {c.name}</span>
              <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{c.sourceFile}</span>
            </div>
          ))}
        </Section>
      )}

      {gaps && gaps.length > 0 && (
        <Section title={`Gaps (${gaps.length})`}>
          {gaps.map((g, i) => (
            <div key={i} className="ar-task-item">
              <StatusBadge status={g.priority} />
              <span>{g.file}</span>
              <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{g.reason}</span>
            </div>
          ))}
        </Section>
      )}

      {staleCases && staleCases.length > 0 && (
        <Section title={`Stale Cases (${staleCases.length})`}>
          {staleCases.map((s, i) => (
            <div key={i} className="ar-task-item">
              <span style={{ color: 'var(--accent-orange)' }}>{'\u26A0'}</span>
              <span>{s.caseId}</span>
              <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{s.sourceFile}</span>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Work Memory ─────────────────────────────────────

function WorkMemoryRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const sessions = (data as any).sessions as Array<{
    id: string; date: string; duration: string; workstream: string; phase: string
    accomplished: string[]; status: string
  }> | undefined
  const resumePoint = (data as any).resumePoint as {
    immediateNextStep: string; context: string
  } | undefined

  return (
    <div className="ar-container">
      <div className="ar-stats-row">
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.totalSessions || 0}</span><span className="ar-stat-chip-label">Sessions</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.currentPhase || '\u2014'}</span><span className="ar-stat-chip-label">Phase</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.momentum || '\u2014'}</span><span className="ar-stat-chip-label">Momentum</span></div>
      </div>

      {resumePoint && (
        <Section title="Resume Point">
          <div className="ar-card" style={{ borderLeftColor: 'var(--accent-green)' }}>
            <div className="ar-card-header"><span className="ar-card-title">{resumePoint.immediateNextStep}</span></div>
            <div className="ar-card-body">{resumePoint.context}</div>
          </div>
        </Section>
      )}

      {sessions && (
        <Section title="Sessions">
          {sessions.slice().reverse().map(s => (
            <div key={s.id} className="ar-card">
              <div className="ar-card-header">
                <span className="ar-card-title">{s.date} — {s.workstream}</span>
                <div style={{ display: 'flex', gap: 6 }}>
                  <StatusBadge status={s.phase} />
                  <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{s.duration}</span>
                </div>
              </div>
              <div className="ar-checklist">
                {s.accomplished.map((a, i) => (
                  <div key={i} className="ar-checklist-item"><span style={{ color: 'var(--accent-green)' }}>{'\u2713'}</span> {a}</div>
                ))}
              </div>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Scale Ready ─────────────────────────────────────

function ScaleReadyRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const _categories = (data as any).categories as Array<{
    id: string; name: string; checks: Array<{ id: string; name: string; status: string; severity: string }>
  }> | undefined
  void _categories // available for future detailed category view
  const blockers = (data as any).blockers as Array<{ name: string; severity: string; recommendation: string }> | undefined

  const counts = summary?.counts || {}

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <StatusBadge status={summary?.overallStatus || 'unknown'} />
        <div className="ar-hero-label" style={{ marginTop: 8 }}>Tier: {summary?.tier || '\u2014'}</div>
      </div>

      <div className="ar-stats-row">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} className="ar-stat-chip">
            <span className="ar-stat-chip-value">{String(v)}</span>
            <span className="ar-stat-chip-label">{k}</span>
          </div>
        ))}
      </div>

      {summary?.categoryScores && (
        <Section title="Categories">
          {Object.entries(summary.categoryScores).map(([cat, scores]: [string, any]) => {
            const total = (scores.pass || 0) + (scores.warning || 0) + (scores.fail || 0) + (scores['human-verify'] || 0)
            const passRate = total > 0 ? Math.round(((scores.pass || 0) / total) * 100) : 0
            return (
              <div key={cat} className="ar-task-item">
                <span style={{ minWidth: 120, fontWeight: 500 }}>{cat}</span>
                <ProgressBar value={passRate} />
                <span style={{ fontSize: 11, color: 'var(--text-dim)', minWidth: 80, textAlign: 'right' }}>
                  {scores.pass}P {scores.warning}W {scores.fail}F
                </span>
              </div>
            )
          })}
        </Section>
      )}

      {blockers && blockers.length > 0 && (
        <Section title={`Blockers (${blockers.length})`}>
          {blockers.map((b, i) => (
            <div key={i} className="ar-card" style={{ borderLeftColor: 'var(--accent-red)' }}>
              <div className="ar-card-header">
                <span className="ar-card-title">{b.name}</span>
                <StatusBadge status={b.severity} />
              </div>
              {b.recommendation && <div className="ar-card-note" style={{ color: 'var(--accent-green)' }}>{b.recommendation}</div>}
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Bug Spec ────────────────────────────────────────

function BugSpecRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const investigation = (data as any).investigation as {
    rootCause?: string; blastRadius?: string; codePath?: string[]
  } | undefined
  const fix = (data as any).fix as { description?: string; approach?: string } | undefined

  return (
    <div className="ar-container">
      <div className="ar-hero">
        <div className="ar-hero-score" style={{ color: 'var(--accent-red)', fontSize: 24 }}>{summary?.name || 'Bug'}</div>
        <StatusBadge status={summary?.status || 'open'} />
      </div>

      {investigation && (
        <Section title="Investigation">
          {investigation.rootCause && (
            <div className="ar-card">
              <div className="ar-card-header"><span className="ar-card-title">Root Cause</span></div>
              <div className="ar-card-body">{investigation.rootCause}</div>
            </div>
          )}
          {investigation.blastRadius && (
            <div className="ar-card">
              <div className="ar-card-header"><span className="ar-card-title">Blast Radius</span></div>
              <div className="ar-card-body">{investigation.blastRadius}</div>
            </div>
          )}
        </Section>
      )}

      {fix && (
        <Section title="Fix">
          <div className="ar-card" style={{ borderLeftColor: 'var(--accent-green)' }}>
            <div className="ar-card-body">{fix.description || fix.approach || 'No fix documented'}</div>
          </div>
        </Section>
      )}
    </div>
  )
}

// ─── Prompt Audit ────────────────────────────────────

function PromptAuditRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const prompts = (data as any).prompts as Array<{
    id: string; location: string; provider: string; purpose: string; pipelineType: string; score: number
    issues: Array<{ id: string; dimension: string; severity: string; title: string; fix: string }>
  }> | undefined
  const pipelinesData = (data as any).pipelines as Array<{
    id: string; name: string; type: string
    stages: Array<{ id: string; purpose: string; provider: string }>
    edges: Array<{ id: string; validated: boolean }>
    issues?: string[]
  }> | undefined
  const patterns = (data as any).patterns as {
    antiPatterns?: Array<{ name: string; instances: number; files: string[]; description: string }>
    positivePatterns?: Array<{ name: string; instances: number; description: string }>
  } | undefined
  const recommendations = (data as any).recommendations as Array<{
    priority: string; title: string; description: string; effort: string
  }> | undefined

  const bySeverity = summary?.bySeverity || {}
  const pipelineCounts = summary?.pipelines || {}

  return (
    <div className="ar-container">
      <div className="ar-stats-row">
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.totalPromptsAudited || 0}</span><span className="ar-stat-chip-label">Audited</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{summary?.totalIssuesFound || 0}</span><span className="ar-stat-chip-label">Issues</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{pipelineCounts.multiStage || 0}</span><span className="ar-stat-chip-label">Pipelines</span></div>
        <div className="ar-stat-chip"><span className="ar-stat-chip-value">{(summary?.providers || []).length}</span><span className="ar-stat-chip-label">Providers</span></div>
      </div>

      {(bySeverity.critical > 0 || bySeverity.shouldFix > 0 || bySeverity.minor > 0) && (
        <div className="ar-stats-row">
          {bySeverity.critical > 0 && <div className="ar-stat-chip"><span className="ar-stat-chip-value" style={{ color: 'var(--accent-red)' }}>{bySeverity.critical}</span><span className="ar-stat-chip-label">Critical</span></div>}
          {bySeverity.shouldFix > 0 && <div className="ar-stat-chip"><span className="ar-stat-chip-value" style={{ color: 'var(--accent-orange)' }}>{bySeverity.shouldFix}</span><span className="ar-stat-chip-label">Should Fix</span></div>}
          {bySeverity.minor > 0 && <div className="ar-stat-chip"><span className="ar-stat-chip-value" style={{ color: 'var(--text-muted)' }}>{bySeverity.minor}</span><span className="ar-stat-chip-label">Minor</span></div>}
        </div>
      )}

      {pipelinesData && pipelinesData.length > 0 && (
        <Section title={`Pipelines (${pipelinesData.length})`}>
          {pipelinesData.map(p => {
            const unvalidatedEdges = p.edges.filter(e => !e.validated).length
            return (
              <div key={p.id} className="ar-card" style={{
                borderLeftColor: p.issues && p.issues.length > 0 ? 'var(--accent-orange)' : 'var(--accent-green)',
              }}>
                <div className="ar-card-header">
                  <span className="ar-card-title">{p.name}</span>
                  <div style={{ display: 'flex', gap: 6 }}>
                    <StatusBadge status={p.type} />
                    <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{p.stages.length} stages</span>
                  </div>
                </div>
                {unvalidatedEdges > 0 && (
                  <div className="ar-card-note" style={{ color: 'var(--accent-red)' }}>
                    {unvalidatedEdges} unvalidated data flow{unvalidatedEdges > 1 ? 's' : ''}
                  </div>
                )}
              </div>
            )
          })}
        </Section>
      )}

      {prompts && prompts.length > 0 && (
        <Section title={`Integration Points (${prompts.length})`}>
          {prompts.map(p => (
            <div key={p.id} className="ar-task-item">
              <span style={{
                fontWeight: 600, minWidth: 28, textAlign: 'center',
                color: p.score >= 8 ? 'var(--accent-green)' : p.score >= 5 ? 'var(--accent-orange)' : 'var(--accent-red)',
              }}>{p.score}</span>
              <StatusBadge status={p.pipelineType} />
              <span style={{ flex: 1, fontSize: 12 }}>{p.purpose}</span>
              <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{p.provider}</span>
              {p.issues.length > 0 && (
                <span style={{ fontSize: 10, color: 'var(--accent-red)' }}>{p.issues.length} issue{p.issues.length > 1 ? 's' : ''}</span>
              )}
            </div>
          ))}
        </Section>
      )}

      {patterns?.antiPatterns && patterns.antiPatterns.length > 0 && (
        <Section title="Anti-Patterns Found">
          {patterns.antiPatterns.map((p, i) => (
            <div key={i} className="ar-card" style={{ borderLeftColor: 'var(--accent-red)' }}>
              <div className="ar-card-header">
                <span className="ar-card-title">{p.name}</span>
                <span style={{ color: 'var(--accent-red)', fontSize: 12 }}>{p.instances}x</span>
              </div>
              <div className="ar-card-body">{p.description}</div>
              <div className="ar-card-note" style={{ fontFamily: 'monospace', fontSize: 11 }}>{p.files.join(', ')}</div>
            </div>
          ))}
        </Section>
      )}

      {patterns?.positivePatterns && patterns.positivePatterns.length > 0 && (
        <Section title="Positive Patterns">
          {patterns.positivePatterns.map((p, i) => (
            <div key={i} className="ar-task-item">
              <span style={{ color: 'var(--accent-green)' }}>{'\u2713'}</span>
              <span style={{ flex: 1 }}>{p.name}</span>
              <span style={{ color: 'var(--accent-green)' }}>{p.instances}x</span>
            </div>
          ))}
        </Section>
      )}

      {recommendations && recommendations.length > 0 && (
        <Section title="Recommendations">
          {recommendations.map((r, i) => (
            <div key={i} className="ar-card" style={{
              borderLeftColor: r.priority === 'critical' ? 'var(--accent-red)' : r.priority === 'shouldFix' ? 'var(--accent-orange)' : 'var(--text-muted)',
            }}>
              <div className="ar-card-header">
                <span className="ar-card-title">{r.title}</span>
                <div style={{ display: 'flex', gap: 6 }}>
                  <StatusBadge status={r.priority} />
                  <StatusBadge status={r.effort} />
                </div>
              </div>
              <div className="ar-card-body">{r.description}</div>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── UX Decisions ────────────────────────────────────

function UxDecisionsRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const decisions = (data as any).decisions as Array<{
    pattern: string; rationale: string; checklist?: string[]
  }> | undefined

  return (
    <div className="ar-container">
      <div className="ar-stats-row">
        {summary?.byCategory && Object.entries(summary.byCategory).map(([k, v]) => (
          <div key={k} className="ar-stat-chip">
            <span className="ar-stat-chip-value">{String(v)}</span>
            <span className="ar-stat-chip-label">{k}</span>
          </div>
        ))}
      </div>

      {decisions && (
        <Section title={`Decisions (${decisions.length})`}>
          {decisions.map((d, i) => (
            <div key={i} className="ar-card">
              <div className="ar-card-header"><span className="ar-card-title">{d.pattern}</span></div>
              <div className="ar-card-body">{d.rationale}</div>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── User Tasks ──────────────────────────────────────

function UserTasksRenderer({ data }: RendererProps) {
  const summary = data.summary as any
  const tasks = (data as any).tasks as Array<{
    title: string; status: string; priority: string; description?: string
  }> | undefined

  return (
    <div className="ar-container">
      <div className="ar-stats-row">
        {summary?.byStatus && Object.entries(summary.byStatus).map(([k, v]) => (
          <div key={k} className="ar-stat-chip">
            <span className="ar-stat-chip-value">{String(v)}</span>
            <span className="ar-stat-chip-label">{k}</span>
          </div>
        ))}
      </div>

      {tasks && (
        <Section title={`Tasks (${tasks.length})`}>
          {tasks.map((t, i) => (
            <div key={i} className="ar-task-item">
              <StatusBadge status={t.status} />
              <StatusBadge status={t.priority} />
              <span style={{ flex: 1 }}>{t.title}</span>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Project Why ─────────────────────────────────────

function ProjectWhyRenderer({ data }: RendererProps) {
  const vision = (data as any).vision as string | undefined
  const problem = (data as any).problem as string | undefined
  const approach = (data as any).approach as string | undefined
  const constraints = (data as any).constraints as string[] | undefined

  return (
    <div className="ar-container">
      {vision && (
        <Section title="Vision">
          <div className="ar-card" style={{ borderLeftColor: 'var(--accent-blue)' }}>
            <div className="ar-card-body" style={{ fontSize: 15 }}>{vision}</div>
          </div>
        </Section>
      )}
      {problem && (
        <Section title="Problem">
          <div className="ar-card" style={{ borderLeftColor: 'var(--accent-red)' }}>
            <div className="ar-card-body">{problem}</div>
          </div>
        </Section>
      )}
      {approach && (
        <Section title="Approach">
          <div className="ar-card" style={{ borderLeftColor: 'var(--accent-green)' }}>
            <div className="ar-card-body">{approach}</div>
          </div>
        </Section>
      )}
      {constraints && constraints.length > 0 && (
        <Section title="Constraints">
          <div className="ar-checklist">
            {constraints.map((c, i) => (
              <div key={i} className="ar-checklist-item"><span style={{ color: 'var(--accent-orange)' }}>{'\u26A0'}</span> {c}</div>
            ))}
          </div>
        </Section>
      )}
    </div>
  )
}

// ─── Codebase Index ──────────────────────────────────

function CodebaseIndexRenderer({ data }: RendererProps) {
  const framework = (data as any).framework as { name?: string; version?: string } | undefined
  const entryPoints = (data as any).entryPoints as string[] | undefined
  const directories = (data as any).directories as Array<{ path: string; purpose?: string }> | undefined
  const scripts = (data as any).scripts as Record<string, string> | undefined

  return (
    <div className="ar-container">
      {framework && (
        <div className="ar-stats-row">
          <div className="ar-stat-chip"><span className="ar-stat-chip-value">{framework.name || '\u2014'}</span><span className="ar-stat-chip-label">Framework</span></div>
          {framework.version && <div className="ar-stat-chip"><span className="ar-stat-chip-value">{framework.version}</span><span className="ar-stat-chip-label">Version</span></div>}
        </div>
      )}

      {entryPoints && (
        <Section title="Entry Points">
          <div className="ar-checklist">
            {entryPoints.map((e, i) => (
              <div key={i} className="ar-checklist-item" style={{ fontFamily: 'monospace', fontSize: 12 }}>{e}</div>
            ))}
          </div>
        </Section>
      )}

      {directories && (
        <Section title="Directories">
          {directories.map((d, i) => (
            <div key={i} className="ar-task-item">
              <span style={{ fontFamily: 'monospace', fontSize: 12, color: 'var(--accent-blue)' }}>{d.path}</span>
              {d.purpose && <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{d.purpose}</span>}
            </div>
          ))}
        </Section>
      )}

      {scripts && (
        <Section title="Scripts">
          {Object.entries(scripts).map(([name, cmd]) => (
            <div key={name} className="ar-task-item">
              <span style={{ fontFamily: 'monospace', fontSize: 12, color: 'var(--accent-green)', minWidth: 100 }}>{name}</span>
              <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{String(cmd)}</span>
            </div>
          ))}
        </Section>
      )}
    </div>
  )
}

// ─── Fallback ────────────────────────────────────────

function FallbackRenderer({ data }: RendererProps) {
  return (
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
  )
}
