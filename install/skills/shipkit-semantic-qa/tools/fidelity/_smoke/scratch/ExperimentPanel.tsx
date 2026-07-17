// Fixture surface: NOT declared anywhere in spec.json. Scratch/experiment code
// carrying high-confidence seams. The gate must NOT fail on it — nobody declared
// it live, so it is advisory only (declaredLive: false).
//
// This is the v1 precision bug in miniature: seams in undeclared files like this
// one are exactly what dragged measured precision to ~27-30%. Exercises the
// fail-open path in _declared.classify_file().
import { mockExperimentRows } from "../mocks/experiments";

const USE_MOCK = true;

export function ExperimentPanel() {
  // TODO: wire up to the real experiments API if we ever ship this
  const rows = USE_MOCK ? mockExperimentRows : [];
  return <DataTable rows={rows} columns={cols} />;
}
