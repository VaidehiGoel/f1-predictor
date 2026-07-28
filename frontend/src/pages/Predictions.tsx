import { useEffect, useState } from "react";
import type { RaceOption, DriverPrediction } from "../types/prediction";
import { getAvailableRaces, getPrediction } from "../api/client";
import PredictionTable from "../components/PredictionTable";

function Predictions() {
  const [races, setRaces] = useState<RaceOption[]>([]);
  const [selectedRace, setSelectedRace] = useState<RaceOption | null>(null);
  const [predictions, setPredictions] = useState<DriverPrediction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAvailableRaces().then((data) => {
      setRaces(data);
      if (data.length > 0) setSelectedRace(data[data.length - 1]);
    });
  }, []);

  async function handlePredict() {
    if (!selectedRace) return;
    setLoading(true);
    setError(null);
    try {
      const result = await getPrediction(
        selectedRace.year,
        selectedRace.round_number,
        selectedRace.event_name
      );
      setPredictions(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1 className="font-display font-black text-4xl mb-2">Race Predictions</h1>
      <p className="text-muted mb-8">
        Select a race with completed qualifying to generate a predicted finishing order.
      </p>

      <div className="flex gap-3 mb-8">
        <select
          className="bg-surface border border-white/10 rounded-sm px-4 py-2 font-mono text-sm flex-1"
          value={selectedRace ? `${selectedRace.year}-${selectedRace.round_number}` : ""}
          onChange={(e) => {
            const race = races.find(
              (r) => `${r.year}-${r.round_number}` === e.target.value
            );
            setSelectedRace(race ?? null);
          }}
        >
          {races.map((race) => (
            <option key={`${race.year}-${race.round_number}`} value={`${race.year}-${race.round_number}`}>
              Round {race.round_number} — {race.event_name} ({race.year})
            </option>
          ))}
        </select>
        <button
          onClick={handlePredict}
          disabled={loading || !selectedRace}
          className="bg-race-red font-display font-bold uppercase tracking-wider px-6 py-2 rounded-sm hover:bg-red-600 transition-colors disabled:opacity-50"
        >
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {error && (
        <div className="bg-race-red/10 border border-race-red/30 text-race-red rounded-sm px-4 py-3 mb-6 font-mono text-sm">
          {error}
        </div>
      )}

      {predictions.length > 0 && <PredictionTable predictions={predictions} />}
    </div>
  );
}

export default Predictions;