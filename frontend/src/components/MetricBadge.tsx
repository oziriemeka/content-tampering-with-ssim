import React from "react";

export default function MetricBadge({ ssim }: { ssim: number }) {
  const tamper = Math.min(1, Math.max(0, 1 - ssim));
  const tamperPct = (tamper * 100).toFixed(1);

  let label = "Low tampering";
  let desc = "Looks clean";
  let bg = "bg-emerald-100 text-emerald-800";

  // Tolerance: treat SSIM >= 0.98 as negligible changes
  if (ssim >= 0.98) {
    label = "No tampering";
    desc = "Negligible changes (tolerance)";
    bg = "bg-emerald-100 text-emerald-800";
  }

  else if (tamper >= 0.2) {
    label = "High tampering";
    desc = "Needs human review";
    bg = "bg-red-100 text-red-800";
  } else if (tamper >= 0.08) {
    label = "Possible tampering";
    desc = "Review recommended";
    bg = "bg-amber-100 text-amber-900";
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="rounded bg-slate-100 px-2 py-1 text-slate-800">
        SSIM: {ssim.toFixed(4)}
      </span>
      <span className={`rounded px-2 py-1 ${bg}`}>
        {label} · {tamperPct}% difference
      </span>
      <span className="text-sm text-slate-600">{desc}</span>
      <span
        className="text-sm text-slate-500 underline decoration-dotted cursor-help"
        title={
          "SSIM >= 0.98 is treated as negligible changes to reduce false positives. " +
          "Low scores can come from scanning/compression. Use the heatmap to check critical areas."
        }
      >
        What do these mean?
      </span>
    </div>
  );
}


