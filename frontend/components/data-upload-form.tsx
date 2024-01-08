"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
import { upload } from "@/lib/http";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { parseFile, parseDateId, parseComments, parseSearches, parseShares } from "@/utils/data-parse";

interface DataUploadFormProps extends React.HTMLAttributes<HTMLDivElement> {
  onProcessedData: (data: any) => void;
}

/**
 * Form to upload data.
 * 
 * @param onProcessedData - Function to handle processed data.
 * @param className - CSS classes for the component.
 * @param props - Other HTML attributes for the component.
 * @returns A React component.
 */
export function DataUploadForm({ onProcessedData, className, ...props }: DataUploadFormProps) {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const allParsedData : any = {};

  const handleFileProcessing = async (file: File, fileType: string) => {
    try {
      const fileContent = await parseFile(file);
      let parsedData;
      switch (fileType) {
        case 'browsing':
          parsedData = parseDateId(fileContent as string);
          console.log("Browsing data:", parsedData);
          break;
        case 'like':
          parsedData = parseDateId(fileContent as string);
          console.log("Like data:", parsedData);
          break;
        case 'favorite':
          parsedData = parseDateId(fileContent as string);
          console.log("Favorite data:", parsedData);
          break;
        case 'comment':
          parsedData = parseComments(fileContent as string);
          console.log("Comment data:", parsedData);
          break;
        case 'search':
          parsedData = parseSearches(fileContent as string);
          console.log("Search data:", parsedData);  
          break;
        case 'share':
          parsedData = parseShares(fileContent as string);
          console.log("Share data:", parsedData);
          break;
        default:
          throw new Error("Unknown file type");
      }
      allParsedData[fileType] = parsedData;
    } catch (error) {
      console.error("Error processing file:", error);
    }
  };

  const onSubmit = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const browsingHistory = (
      document.getElementById("browsing") as HTMLInputElement
    ).files![0];
    const likeHistory = (document.getElementById("like") as HTMLInputElement)
      .files![0];
    const favoriteHistory = (
      document.getElementById("favorite") as HTMLInputElement
    ).files![0];
    const commentHistory = (
      document.getElementById("comment") as HTMLInputElement
    ).files![0];
    const searchHistory = (
      document.getElementById("search") as HTMLInputElement
    ).files![0];
    const shareHistory = (document.getElementById("share") as HTMLInputElement)
      .files![0];

    const historyFiles = [
      { 'browsing': browsingHistory },
      { 'like': likeHistory },
      { 'favorite': favoriteHistory },
      { 'comment': commentHistory },
      { 'search': searchHistory },
      { 'share': shareHistory }
    ];

    try {
      for (const historyFile of historyFiles) {
        const fileInput = Object.values(historyFile)[0] as File;
        if (fileInput) {
          const file_id = Object.keys(historyFile)[0];
          await handleFileProcessing(fileInput, file_id);
          console.log("File uploaded for", file_id);
        }
        else {
          console.error("No file uploaded for", Object.keys(historyFile)[0]);
        }
      }

      onProcessedData(allParsedData);
      // const response = await upload(
      //   browsingHistory,
      //   likeHistory,
      //   favoriteHistory,
      //   commentHistory,
      //   searchHistory,
      //   shareHistory
      // );
      // console.log("Upload successful:", response);
    } catch (error) {
      console.error("An error occurred:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <form onSubmit={onSubmit}>
        <div className="grid gap-2">
          <div className="grid gap-1">
            <Label htmlFor="browsing">Browsing History</Label>
            <Input id="browsing" type="file" disabled={isLoading} />
          </div>
          <div className="grid gap-1">
            <Label htmlFor="like">Like History</Label>
            <Input id="like" type="file" disabled={isLoading} />
          </div>
          <div className="grid gap-1">
            <Label htmlFor="favorite">Favorite History</Label>
            <Input id="favorite" type="file" disabled={isLoading} />
          </div>
          <div className="grid gap-1">
            <Label htmlFor="comment">Comment History</Label>
            <Input id="comment" type="file" disabled={isLoading} />
          </div>
          <div className="grid gap-1">
            <Label htmlFor="search">Search History</Label>
            <Input id="search" type="file" disabled={isLoading} />
          </div>
          <div className="grid gap-1">
            <Label htmlFor="share">Share History</Label>
            <Input id="share" type="file" disabled={isLoading} />
          </div>
          <Button type="submit" disabled={isLoading}>
            Upload
          </Button>
        </div>
      </form>
    </div>
  );
}
