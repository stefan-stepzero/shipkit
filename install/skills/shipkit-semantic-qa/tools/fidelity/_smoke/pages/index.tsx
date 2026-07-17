// Fixture: a REAL surface backed by supabase (should classify 'real').
import { createClient } from "@supabase/supabase-js";
const supabase = createClient(url, key);

export default async function Home() {
  const { data } = await supabase.from("students").select("*");
  return <StudentList rows={data} />;
}
