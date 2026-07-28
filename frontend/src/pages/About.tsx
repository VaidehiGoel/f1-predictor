function About() {
  const metrics = [
    { label: "Spearman (all races)", value: "0.649", note: "Includes DNF chaos" },
    { label: "Spearman (finished only)", value: "0.771", note: "Isolates genuine ranking skill" },
    { label: "MAE", value: "10.5", note: "Raw ranker score, not position-scale" },
    { label: "Training window", value: "2022–2025", note: "Tested on full 2025 season" },
  ];

  const features = [
    { name: "Grid Position", desc: "Starting position from qualifying" },
    { name: "Qualifying Pace", desc: "Q1 / Q2 / Q3 lap times in seconds" },
    { name: "Recent Driver Form", desc: "Rolling average finish, last 5 races" },
    { name: "Recent Team Form", desc: "Rolling team average, computed per race weekend" },
    { name: "Circuit History", desc: "Driver's historical average at this specific track" },
    { name: "Teammate Gap", desc: "Recent finishing gap vs. same-car teammate" },
    { name: "Team Reliability", desc: "Rolling DNF rate for the team" },
  ];

  return (
    <div>
      <h1 className="font-display font-black text-4xl mb-2">The Model</h1>
      <p className="text-muted mb-10 max-w-2xl">
        A gradient-boosted ranking model (XGBRanker) trained on five seasons of
        real F1 qualifying and race data, evaluated honestly — including where
        it struggles.
      </p>

      <h2 className="font-display font-bold uppercase tracking-wide text-sm text-telemetry-blue mb-4">
        Evaluation
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-white/5 mb-12 rounded-sm overflow-hidden">
        {metrics.map((m) => (
          <div key={m.label} className="bg-surface px-5 py-4">
            <div className="font-mono text-2xl font-bold text-race-red">{m.value}</div>
            <div className="text-xs uppercase tracking-wide text-muted mt-1">{m.label}</div>
            <div className="text-xs text-muted/70 mt-1">{m.note}</div>
          </div>
        ))}
      </div>

      <h2 className="font-display font-bold uppercase tracking-wide text-sm text-telemetry-blue mb-4">
        Features
      </h2>
      <div className="bg-surface rounded-sm border border-white/5 overflow-hidden mb-12">
        {features.map((f) => (
          <div key={f.name} className="flex px-5 py-3 border-b border-white/5 last:border-0">
            <span className="font-mono text-sm text-ink w-48 shrink-0">{f.name}</span>
            <span className="text-muted text-sm">{f.desc}</span>
          </div>
        ))}
      </div>

      <h2 className="font-display font-bold uppercase tracking-wide text-sm text-telemetry-blue mb-4">
        Honest limitations
      </h2>
      <ul className="text-muted text-sm space-y-2 max-w-2xl list-disc list-inside">
        <li>DNFs (crashes, mechanical failures) are fundamentally unpredictable from pre-race data — they account for most of the gap between the two Spearman scores above.</li>
        <li>Predictions require completed qualifying data; the model does not forecast weeks in advance.</li>
        <li>New teams and drivers with limited history fall back to population averages until real data accumulates.</li>
      </ul>
    </div>
  );
}

export default About;