"use client";

import Image from "next/image";
import { cn } from "@/lib/utils";

interface WowLogoProps {
  variant?: "full" | "icon";
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
  dark?: boolean;
}

const SIZES = {
  sm: { width: 60, height: 34 },
  md: { width: 90, height: 52 },
  lg: { width: 130, height: 74 },
  xl: { width: 180, height: 103 },
};

export default function WowLogo({ variant = "full", size = "md", className, dark }: WowLogoProps) {
  const { width, height } = SIZES[size];

  if (variant === "icon") {
    return (
      <div className={cn("flex items-center gap-2", className)}>
        <Image src="/wow-logo.svg" alt="WoW" width={width} height={height} priority />
      </div>
    );
  }

  return (
    <div className={cn("flex flex-col items-start", className)}>
      <Image src="/wow-logo.svg" alt="WoW — Water on Way" width={width} height={height} priority />
      {size !== "sm" && (
        <span className={cn(
          "text-[10px] font-medium tracking-wide mt-0.5",
          dark ? "text-white/70" : "text-text-secondary"
        )}>
          that&apos;s water on way
        </span>
      )}
    </div>
  );
}
