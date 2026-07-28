import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="py-12">
      <div className="flex items-center gap-3 mb-6">
        <span className="w-2 h-2 bg-race-red rounded-full animate-pulse" />
        <span className="font-mono text-xs uppercase tracking-widest text-muted">
          Live model · 2026 season
        </span>
      </div>

      <h1 className="font-display font-black text-6xl leading-none mb-6">
        PREDICTING THE
        <br />
        <span className="text-race-red">FINISHING ORDER</span>
      </h1>

      <p className="text-muted text-lg max-w-xl mb-10">
        A machine learning model trained on qualifying pace, driver form, team
        reliability, and circuit history — built to rank every driver on the
        grid before lights out.
      </p>

      <Link
        to="/predictions"
        className="inline-block bg-race-red font-display font-bold uppercase tracking-wider px-8 py-3 rounded-sm hover:bg-red-600 transition-colors"
      >
        Run a Prediction →
      </Link>

      <div className="grid grid-cols-3 gap-px bg-white/5 mt-16 rounded-sm overflow-hidden">
        {[
          { label: "Spearman (finished)", value: "0.77" },
          { label: "Seasons trained on", value: "2022–26" },
          { label: "Engineered features", value: "13" },
        ].map((stat) => (
          <div key={stat.label} className="bg-surface px-6 py-5">
            <div className="font-mono text-3xl font-bold text-telemetry-blue">
              {stat.value}
            </div>
            <div className="text-xs text-muted uppercase tracking-wide mt-1">
              {stat.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;