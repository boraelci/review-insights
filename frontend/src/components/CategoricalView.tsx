import * as React from 'react';
import { Radar } from 'react-chartjs-2';

import {
  Chart as ChartJS,
  RadialLinearScale,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

import { CategoricalDataModel } from '.';

interface CategoricalViewProps {
  categoricalDataModel: CategoricalDataModel;
}

export function CategoricalView(props: CategoricalViewProps) {
  ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Title,
    Filler,
    Tooltip,
    Legend,
  );

  const positives = props.categoricalDataModel.positives;
  const negatives = props.categoricalDataModel.negatives;

  const labels: string[] = [];
  const positiveCounts: number[] = [];
  const negativeCounts: number[] = [];

  // Get all unique dates from both positiveData and negativeData
  const uniqueCategories = new Set([
    ...Object.keys(positives),
    ...Object.keys(negatives),
  ]);

  // Fill the labels, positiveCounts, and negativeCounts arrays
  for (const category of Array.from(uniqueCategories)) {
    labels.push(category);
    positiveCounts.push(positives[category] || 0);
    negativeCounts.push(negatives[category] || 0);
  }

  const title = 'Review Counts by Category';
  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: !!title, text: title },
    },
  };

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Positive',
        data: positiveCounts,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Negative',
        data: negativeCounts,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  return <Radar options={options} data={data} />;
}
