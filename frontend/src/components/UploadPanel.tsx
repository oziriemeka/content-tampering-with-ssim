import React, { useEffect, useState } from "react";
import { analyze, AnalyzeResponse } from "../lib/api";
import MetricBadge from "./MetricBadge";
import ResultOverlay from "./ResultOverlay";

export default function UploadPanel() {
  const [reference, setReference] = useState<File | null>(null);
  const [suspect, setSuspect] = useState<File | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [refUrl, setRefUrl] = useState<string | null>(null);
  const [susUrl, setSusUrl] = useState<string | null>(null);

  useEffect(() => {
    if (reference) {
      const url = URL.createObjectURL(reference);
      setRefUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setRefUrl(null);
    }
  }, [reference]);

  useEffect(() => {
    if (suspect) {
      const url = URL.createObjectURL(suspect);
      setSusUrl(url);
      return () => URL.revokeObjectURL(url);
    } else {
      setSusUrl(null);
    }
  }, [suspect]);

  const onAnalyze = async () => {
    if (!reference || !suspect) return;
    setLoading(true);
    setError(null);
    try {
      const r = await analyze(reference, suspect);
      setResult(r);
    } catch (e: any) {
      setError(e?.message || "Failed to analyze");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-3">
      <div className="grid gap-1">
        <label className="text-sm font-medium">Reference</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setReference(e.target.files?.[0] || null)}
        />
      </div>
      <div className="grid gap-1">
        <label className="text-sm font-medium">Suspect</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setSuspect(e.target.files?.[0] || null)}
        />
      </div>
      <button
        className="w-full rounded bg-slate-900 px-3 py-2 text-white disabled:opacity-50"
        onClick={onAnalyze}
        disabled={!reference || !suspect || loading}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      {error && <div className="text-red-600">{error}</div>}
      {result && (
        <div className="grid gap-3">
          <MetricBadge ssim={result.ssim_score} />
          <div className="grid gap-3" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", display: "grid", alignItems: "start" }}>
            <div>
              <h3 className="my-2 font-medium">Reference</h3>
              <div className="rounded border bg-white p-2">
                {refUrl ? (
                  <img src={refUrl} alt="Reference" className="max-w-full" />
                ) : (
                  <div className="text-slate-500">No reference selected</div>
                )}
              </div>
            </div>
            <div>
              <h3 className="my-2 font-medium">Suspect</h3>
              <div className="rounded border bg-white p-2">
                {susUrl ? (
                  <img src={susUrl} alt="Suspect" className="max-w-full" />
                ) : (
                  <div className="text-slate-500">No suspect selected</div>
                )}
              </div>
            </div>
            <div>
              <h3 className="my-2 font-medium">Result</h3>
              <div className="rounded border bg-white p-2">
                <ResultOverlay overlayB64={result.overlay_b64} heatmapB64={result.heatmap_b64} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


