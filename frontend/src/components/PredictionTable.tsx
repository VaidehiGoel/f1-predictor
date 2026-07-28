import type { DriverPrediction } from "../types/prediction";

function PredictionTable({ predictions }: { predictions: DriverPrediction[] }) {
  return (
    <div className="bg-surface rounded-sm overflow-hidden border border-white/5">
      <div className="grid grid-cols-[4rem_1fr_1fr_5rem] gap-4 px-5 py-3 font-display uppercase text-xs tracking-widest text-muted border-b border-white/5">
        <span>Pos</span>
        <span>Driver</span>
        <span>Team</span>
        <span className="text-right">Grid</span>
      </div>

      {predictions.map((driver, i) => (
        <div
          key={driver.Abbreviation}
          className="grid grid-cols-[4rem_1fr_1fr_5rem] gap-4 items-center px-5 py-3 border-b border-white/5 last:border-0 hover:bg-surface-light transition-colors"
          style={{
            animation: `fadeInRow 0.4s ease-out ${i * 0.03}s both`,
          }}
        >
          <span className="font-mono text-2xl font-bold text-race-red">
            {String(driver.PredictedRank).padStart(2, "0")}
          </span>
          <div className="flex items-center gap-3">
            <span
              className="w-1 h-8 skew-x-[-12deg]"
              style={{ backgroundColor: driver.TeamColor ? `#${driver.TeamColor}` : "#6B7280" }}
            />
            <div>
              <div className="font-semibold">{driver.FullName}</div>
              <div className="font-mono text-xs text-muted">{driver.Abbreviation}</div>
            </div>
          </div>
          <span className="text-muted text-sm">{driver.TeamName}</span>
          <span className="font-mono text-right text-telemetry-blue">
            P{driver.GridPosition}
          </span>
        </div>
      ))}

      <style>{`
        @keyframes fadeInRow {
          from { opacity: 0; transform: translateX(-8px); }
          to { opacity: 1; transform: translateX(0); }
        }
      `}</style>
    </div>
  );
}

export default PredictionTable;