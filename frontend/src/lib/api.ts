export type Box = { x: number; y: number; w: number; h: number };
export type AnalyzeResponse = {
  ssim_score: number;
  boxes: Box[];
  overlay_b64: string;
  heatmap_b64: string;
  message: string;
};

export async function analyze(reference: File, suspect: File) {
  const fd = new FormData();
  fd.append("reference", reference);
  fd.append("suspect", suspect);
  const base = import.meta.env.VITE_API_URL || "http://localhost:8000";
  const res = await fetch(`${base}/analyze`, {
    method: "POST",
    body: fd,
  });
  if (!res.ok) throw new Error("Analysis failed");
  return (await res.json()) as AnalyzeResponse;
}


