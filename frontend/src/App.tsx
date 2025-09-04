import React from "react";
import UploadPanel from "./components/UploadPanel";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto max-w-5xl px-4 py-4">
          <h1 className="text-3xl font-bold">SSIM Forgery Detection</h1>
          <p className="text-slate-600">Upload reference and suspect images, then analyze differences.</p>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6">
        <UploadPanel />
        <div className="mt-10 text-sm text-slate-600">
          <div className="rounded-md border bg-white p-4">
            <p>
              <span className="font-semibold">Name:</span> Emeka Emmanuel Oziri
            </p>
            <p>
              <span className="font-semibold">Student ID:</span> 24140162
            </p>
            <p>
              <span className="font-semibold">School:</span> Birmingham City University
            </p>
            <p>
              <span className="font-semibold">Supervisor:</span> Yekta Said Can
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}


