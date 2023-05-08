export interface CategoricalDataModelProps {
  positives: { [category: string]: number };
  negatives: { [category: string]: number };
}

export class CategoricalDataModel {
  positives: { [category: string]: number };
  negatives: { [category: string]: number };

  constructor(props: CategoricalDataModelProps) {
    this.positives = props.positives;
    this.negatives = props.negatives;
  }
}
