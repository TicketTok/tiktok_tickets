"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface DataUploadFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function DataUploadForm({ className, ...props }: DataUploadFormProps) {
  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  async function onSubmit(event: React.SyntheticEvent) {
    event.preventDefault();
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  }

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
          <Button
            disabled={isLoading}
            onClick={() => {
              setIsLoading(true);
            }}
          >
            Upload
          </Button>
        </div>
      </form>
    </div>
  );
}
