import * as React from 'react';
import { Line } from 'react-chartjs-2';

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

interface HistoricalViewProps {
  positiveData: { date: string; count: number }[];
  negativeData: { date: string; count: number }[];
}

export function HistoricalView({
  positiveData,
  negativeData,
}: HistoricalViewProps) {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  );

  const title =
    'Historical View for # of Positive and Negative Reviews Over Time';
  // Replace the hardcoded months, positiveCount, and negativeCount
  positiveData.sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime(),
  );
  negativeData.sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime(),
  );

  const labels = positiveData.map((data) => data.date);
  const positiveCount = positiveData.map((data) => data.count);
  const negativeCount = negativeData.map((data) => data.count);

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
        data: positiveCount,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Negative',
        data: negativeCount,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };

  return <Line options={options} data={data} />;
}
