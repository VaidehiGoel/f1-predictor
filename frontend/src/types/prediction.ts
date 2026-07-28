export interface DriverPrediction {
  Abbreviation: string;
  FullName: string;
  TeamName: string;
  TeamColor: string;
  GridPosition: number;
  PredictedRank: number;
}

export interface RaceOption {
  year: number;
  round_number: number;
  event_name: string;
}