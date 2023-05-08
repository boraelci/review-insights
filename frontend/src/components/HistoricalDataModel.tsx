export interface HistoricalDataModelProps {
  positives: { [date: string]: number };
  negatives: { [date: string]: number };
}

export class HistoricalDataModel {
  positives: { [date: string]: number };
  negatives: { [date: string]: number };

  constructor(props: HistoricalDataModelProps) {
    this.positives = props.positives;
    this.negatives = props.negatives;
  }
}
