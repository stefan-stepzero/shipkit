// Fixture surface: mimics a phinma staff dashboard on mock data.
import { mockStaffData } from "../mocks/staffData";

const USE_MOCK = true;

export function StaffDashboard() {
  // TODO: wire this up to cohort_leaderboard_v when the view lands
  const rows = USE_MOCK ? mockStaffData : [];
  const grade_band = rows.map(r => (r.score >= 80 ? "A" : r.score >= 60 ? "B" : "C"));
  return (
    <DataTable columns={cols} rows={rows} dataKey="id" band={grade_band} />
  );
}
