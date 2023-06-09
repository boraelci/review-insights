import * as React from 'react';
import { Line } from 'react-chartjs-2';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

import { HistoricalDataModel } from '.';

interface HistoricalViewProps {
  historicalDataModel: HistoricalDataModel;
}

export function HistoricalView(props: HistoricalViewProps) {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  );

  const positives = props.historicalDataModel.positives;
  const negatives = props.historicalDataModel.negatives;

  const labels: string[] = [];
  const positiveCounts: number[] = [];
  const negativeCounts: number[] = [];

  // Get all unique dates from both positiveData and negativeData
  const uniqueDates = new Set([
    ...Object.keys(positives),
    ...Object.keys(negatives),
  ]);

  // Create a sorted array of dates
  const sortedDates = Array.from(uniqueDates).sort(
    (a, b) => new Date(a).getTime() - new Date(b).getTime(),
  );

  // Fill the labels, positiveCounts, and negativeCounts arrays
  for (const date of sortedDates) {
    labels.push(date);
    positiveCounts.push(positives[date] || 0);
    negativeCounts.push(negatives[date] || 0);
  }

  const title = 'Review Counts by Date';
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

  return <Line options={options} data={data} />;
}
