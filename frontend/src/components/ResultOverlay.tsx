import React, { useState } from "react";

export default function ResultOverlay({ overlayB64, heatmapB64 }: { overlayB64: string; heatmapB64: string }) {
  const [showHeatmap, setShowHeatmap] = useState(false);
  return (
    <div className="grid gap-2">
      <div className="flex items-center gap-3">
        <button
          type="button"
          role="switch"
          aria-checked={showHeatmap}
          onClick={() => setShowHeatmap((v) => !v)}
          className={
            "relative inline-flex h-6 w-11 items-center rounded-full transition-colors " +
            (showHeatmap ? "bg-slate-900" : "bg-slate-300")
          }
        >
          <span className="sr-only">Show heatmap</span>
          <span
            className={
              "inline-block h-5 w-5 transform rounded-full bg-white transition-transform " +
              (showHeatmap ? "translate-x-5" : "translate-x-1")
            }
          />
        </button>
        <span className="text-slate-800">Show heatmap</span>
      </div>
      <img
        src={`data:image/png;base64,${showHeatmap ? heatmapB64 : overlayB64}`}
        alt={showHeatmap ? "Heatmap" : "Overlay"}
        className="h-auto w-full max-w-full rounded border bg-white"
      />
    </div>
  );
}


