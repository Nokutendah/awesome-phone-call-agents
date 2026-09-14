'use client';

import React from 'react';
import Link from 'next/link';
import { ArchitectureDiagram } from '@/components/ArchitectureDiagram';

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-12 space-y-20">
      {/* Header section */}
      <div className="border-b-2 border-black pb-8 space-y-4">
        <span className="text-xs font-mono uppercase tracking-widest text-gray-500 block">
          About The System
        </span>
        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-black uppercase leading-tight">
          A Cross-Functional<br />Architecture for<br />Agentic Calls.
        </h1>
        <p className="text-lg text-gray-700 max-w-3xl leading-relaxed">
          An autonomous system designed to transform natural-language objectives into real-world telephony execution, high-fidelity audio evidence, and verified intelligence.
        </p>
      </div>

      {/* Section 01: The Problem */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
            01 // The Problem
          </span>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            Unindexed Information
          </span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold text-black tracking-tight">
          Critical business intelligence is locked inside real-time phone conversations.
        </h2>
        <p className="text-base text-gray-700 leading-relaxed max-w-3xl">
          Despite decades of web indexing, the vast majority of operational, logistical, and commercial truth exists solely in voice endpoints: inventory availability, special dietary policies, emergency appointments, custom quotes, and real-time support queues. Web scrapers and LLMs cannot access this information without placing live phone calls.
        </p>
      </section>

      {/* Section 02: The Idea */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
            02 // The Idea
          </span>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            End-to-End Orchestration
          </span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold text-black tracking-tight">
          Moving beyond chatbots to cross-functional telephony orchestration.
        </h2>
        <p className="text-base text-gray-700 leading-relaxed max-w-3xl">
          Generic AI voice assistants fail when encountering real-world phone infrastructure. Navigating an automated IVR menu requires DTMF tones; dealing with hold music requires acoustic classification; speaking with busy frontline workers demands low-latency, contextual grounding and strict verification bounds.
        </p>
      </section>

      {/* Section 03: The Architecture */}
      <section className="space-y-6">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
            03 // The Architecture
          </span>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            System Topology
          </span>
        </div>
        <ArchitectureDiagram />
      </section>

      {/* Section 04: Why Phone Calls Matter */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
            04 // Why Phone Calls Matter
          </span>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            Ground-Truth Verification
          </span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold text-black tracking-tight">
          The ultimate verification medium for real-world operations.
        </h2>
        <p className="text-base text-gray-700 leading-relaxed max-w-3xl">
          Direct human conversation provides authoritative, timestamped evidence that outdated websites or static knowledge bases cannot offer. When decisions have financial, legal, or health implications, directly speaking with a representative is the gold standard for confirmation.
        </p>
      </section>

      {/* Section 05: What This Prototype Demonstrates */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
            05 // What This Prototype Demonstrates
          </span>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            Hackathon Scope
          </span>
        </div>
        <div className="space-y-3 text-sm text-gray-700 max-w-3xl leading-relaxed">
          <p>
            This prototype demonstrates the complete pipeline from a natural-language mission prompt to an autonomous CALL-E voice call, live transcript streaming, structured question verification, and an auditable investigation dossier.
          </p>
          <ul className="list-disc pl-5 space-y-1 font-mono text-xs text-gray-800">
            <li>Zero-shot mission planning and question extraction with Gemini</li>
            <li>Simulated or real CALL-E telephony integration with IVR &amp; hold detection</li>
            <li>Real-time telemetry and transcript streaming</li>
            <li>Strict post-call intelligence parsing with verification tags</li>
          </ul>
        </div>
      </section>

      {/* Bottom CTA */}
      <div className="border border-black p-8 sm:p-12 bg-[#F7F7F5] flex flex-col sm:flex-row sm:items-center justify-between gap-6 rounded-3xl">
        <div className="space-y-1">
          <h4 className="text-xl font-bold text-black">Ready to test the pipeline?</h4>
          <p className="text-xs font-mono text-gray-600">
            Create an investigation mission in seconds.
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
