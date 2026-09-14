'use client';

import React from 'react';
import Link from 'next/link';
import { ArchitectureDiagram } from '@/components/ArchitectureDiagram';

export default function ArchitecturePage() {
  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-20">
      {/* Header section */}
      <div className="border-b-2 border-black pb-8 space-y-4">
        <span className="text-xs font-mono uppercase tracking-widest text-gray-500 block">
          Technical Specification // Architecture Dossier
        </span>
        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-black uppercase leading-tight">
          A Cross-Functional<br />Architecture for<br />Agentic Calls
        </h1>
        <p className="text-lg text-gray-700 max-w-3xl leading-relaxed">
          An end-to-end orchestration pipeline bridging natural-language intent, telephony networks, autonomous voice reasoning, evidence capture, and structured fact verification.
        </p>
      </div>

      {/* Primary Visual - The Full Engineering Diagram */}
      <section className="space-y-6">
        <div className="flex items-center justify-between border-b border-gray-200 pb-3">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
            Full System Topology
          </span>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            01 &rarr; 09 Sequential Flow
          </span>
        </div>
        <ArchitectureDiagram />
      </section>

      {/* Deep-Dive Architectural Explanations */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-8 border-t border-gray-200">
        <div className="space-y-4 border border-gray-200 p-6 rounded-2xl bg-[#FAFAF9]">
          <div className="text-xs font-mono font-bold text-gray-500 uppercase tracking-widest">
            Layer A // Planning &amp; Resolution
          </div>
          <h3 className="text-2xl font-bold text-black tracking-tight">
            Intent Decomposition &amp; Pre-Call Grounding
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            When a user provides a high-level goal, Gemini extracts specific factual inquiries, boundary constraints, and entity identifiers. The system resolves business operating conditions, phone endpoints, and timezones before dispatching a dial command.
          </p>
        </div>

        <div className="space-y-4 border border-gray-200 p-6 rounded-2xl bg-[#FAFAF9]">
          <div className="text-xs font-mono font-bold text-gray-500 uppercase tracking-widest">
            Layer B // Telephony &amp; Voice Execution
          </div>
          <h3 className="text-2xl font-bold text-black tracking-tight">
            Low-Latency CALL-E Voice Streaming
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            Real phone systems present unique hurdles: complex IVR trees, long hold queues, ambient noise, and unexpected human conversational branching. The execution layer navigates touch-tone phone trees and negotiates real-time speech over standard telecom trunks.
          </p>
        </div>

        <div className="space-y-4 border border-gray-200 p-6 rounded-2xl bg-[#FAFAF9]">
          <div className="text-xs font-mono font-bold text-gray-500 uppercase tracking-widest">
            Layer C // Evidence Capture
          </div>
          <h3 className="text-2xl font-bold text-black tracking-tight">
            Turn-by-Turn Telephony Telemetry
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            Every audio turn, DTMF digit sent, hold duration, and speaker transition is timestamped and persisted directly to the SQLite local database. This guarantees an immutable audit trail for every completed investigation.
          </p>
        </div>

        <div className="space-y-4 border border-gray-200 p-6 rounded-2xl bg-[#FAFAF9]">
          <div className="text-xs font-mono font-bold text-gray-500 uppercase tracking-widest">
            Layer D // Structured Intelligence
          </div>
          <h3 className="text-2xl font-bold text-black tracking-tight">
            Strict Fact-Checking &amp; Uncertainty Boundaries
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            The post-call intelligence parser is governed by a strict zero-hallucination policy. If a representative did not state a policy or answer with certainty, the claim is explicitly labeled &ldquo;COULD NOT VERIFY&rdquo; rather than inferred.
          </p>
        </div>
      </section>

      {/* CTA Footer */}
      <div className="border border-black p-8 sm:p-12 bg-[#F7F7F5] flex flex-col sm:flex-row sm:items-center justify-between gap-6 rounded-3xl">
        <div className="space-y-1">
          <h4 className="text-xl font-bold text-black">Ready to launch a phone mission?</h4>
          <p className="text-xs font-mono text-gray-600">
            Test the live architecture with your natural-language inquiry.
          </p>
        </div>
        <Link
          href="/"
          className="px-6 py-3 bg-black text-white text-xs font-mono uppercase tracking-wider hover:bg-gray-800 transition-colors whitespace-nowrap self-start sm:self-auto rounded-full"
        >
          Start An Investigation &rarr;
        </Link>
      </div>
    </div>
  );
}
