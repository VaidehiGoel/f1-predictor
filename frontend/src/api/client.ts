import type { DriverPrediction, RaceOption } from "../types/prediction";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function getAvailableRaces(): Promise<RaceOption[]> {
  const response = await fetch(`${API_BASE_URL}/races`);

  if (!response.ok) {
    throw new Error("Failed to fetch available races");
  }

  return response.json();
}

export async function getPrediction(
  year: number,
  roundNumber: number,
  eventName: string
): Promise<DriverPrediction[]> {
  const params = new URLSearchParams({
    year: year.toString(),
    round_number: roundNumber.toString(),
    event_name: eventName,
  });

  const response = await fetch(`${API_BASE_URL}/predict?${params.toString()}`);

  if (!response.ok) {
    const errorBody = await response.json();
    throw new Error(errorBody.detail || "Prediction request failed");
  }

  return response.json();
}