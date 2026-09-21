import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes safely (handles conflicts) */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Format currency in INR */
export function formatINR(amount: number | string): string {
  const num = typeof amount === "string" ? parseFloat(amount) : amount;
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(num);
}

/** Format litres with appropriate suffix */
export function formatLitres(litres: number): string {
  if (litres >= 1000) {
    return `${(litres / 1000).toFixed(litres % 1000 === 0 ? 0 : 1)}KL`;
  }
  return `${litres}L`;
}

/** Format date to readable string */
export function formatDate(date: string | Date, includeTime = false): string {
  const d = new Date(date);
  const opts: Intl.DateTimeFormatOptions = {
    day: "numeric",
    month: "short",
    year: "numeric",
  };
  if (includeTime) {
    opts.hour = "2-digit";
    opts.minute = "2-digit";
  }
  return d.toLocaleDateString("en-IN", opts);
}

/** Format relative time (e.g., "2 hours ago") */
export function formatRelative(date: string | Date): string {
  const now = new Date();
  const d = new Date(date);
  const diffMs = now.getTime() - d.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "Just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.floor(diffHr / 24);
  if (diffDay < 7) return `${diffDay}d ago`;
  return formatDate(date);
}

/** Truncate string with ellipsis */
export function truncate(str: string, maxLen: number): string {
  if (str.length <= maxLen) return str;
  return str.slice(0, maxLen - 1) + "…";
}
