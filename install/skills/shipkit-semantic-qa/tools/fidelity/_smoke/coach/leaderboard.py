# Fixture: grade_band computed a SECOND time here (SSOT risk with the dashboard).
def compute(rows):
    grade_band = "A" if rows["score"] >= 80 else "B" if rows["score"] >= 60 else "C"
    mastery_rate = sum(r["correct"] for r in rows) / max(len(rows), 1)
    return grade_band, mastery_rate
