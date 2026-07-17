// Fixture surface: DEFERRED in spec.json (deferred[].element = "predictive pacing").
// It is stuffed with high-confidence seams on purpose. The gate must NOT fail on
// any of them: a mock seam on an explicitly-deferred surface is fine.
// Exercises the deferred-suppression path in _declared.is_deferred().
import { mockPacingData } from "../mocks/pacing";

const USE_MOCK = true;

export function PredictivePacing() {
  // TODO: wire this up to the real pacing API once the surface is in scope
  const rows = USE_MOCK ? mockPacingData : [];
  return <PacingChart rows={rows} dataKey="week" />;
}
