// Fixture surface: renders data but has NO backing source (missing).
export function ExecView() {
  return (
    <div>
      <MetricCard value={summary.total} />
      {summary.items.map(i => <Row key={i.id} score={i.score} />)}
      <span>coming soon: predictive pacing</span>
    </div>
  );
}
