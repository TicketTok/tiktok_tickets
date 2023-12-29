"use client";

import Link from "next/link";
import React, { useState } from 'react';
import { DataUploadForm } from "@/components/data-upload-form";
import { ModeToggle } from "@/components/ui/mode-toggle";
// import { parseFile } from "@/utils/data-parse";

export default function Home() {
  const [visualizationData, setVisualizationData] = useState(null);

  // Function to handle data from DataUploadForm
  const handleProcessedData = (data: any) => {
    setVisualizationData(data);
    console.log("Data from DataUploadForm:", data);
  };

  return (
    <>
      <div className="container relative hidden h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:px-0">
        <div className="absolute right-4 top-4 md:right-8 md:top-8">
          <ModeToggle />
        </div>
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
          <div className="flex flex-col space-y-2 text-center">
            <h1 className="text-2xl font-semibold tracking-tight">
              Upload your data
            </h1>
            <p className="text-sm text-muted-foreground">
              Don&apos;t have your data? Learn how to get it here.
            </p>
          </div>
          <DataUploadForm onProcessedData={handleProcessedData} />
        </div>
      </div>
    </>
  );
}
