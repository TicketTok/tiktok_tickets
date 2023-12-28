"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
import { upload } from "@/lib/http";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface DataUploadFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function DataUploadForm({ className, ...props }: DataUploadFormProps) {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

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

    try {
      const response = await upload(
        browsingHistory,
        likeHistory,
        favoriteHistory,
        commentHistory,
        searchHistory,
        shareHistory
      );
      console.log("Upload successful:", response);
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
