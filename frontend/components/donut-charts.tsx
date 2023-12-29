"use client";

import { Card, DonutChart, Title } from "@tremor/react";

interface LikedChartProps {
  liked?: any[];
  watched?: any[]
}

export const LikedChart: React.FC<LikedChartProps> = ({ liked, watched }) => {
  const videos: any[] = [
  ];
  const numWatched = watched?.length || 0;
  const numLiked = liked?.length || 0;
  videos.push({ name: "Liked", value: numLiked});
  videos.push({ name: "Not Liked", value: (numWatched - numLiked) });
  const title = `Liked (${numLiked}) vs. Total (${numWatched})`;

  return (
    <Card className="max-w-lg">
      <Title>{title}</Title>
      <DonutChart
        className="mt-6"
        data={videos}
        category="value"
        index="name"
        colors={["rose", "indigo"]} />
    </Card>
  );
};