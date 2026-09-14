'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { ConfirmationModal } from '@/components/ConfirmationModal';
import { LiveCallView } from '@/components/LiveCallView';
import { CaseReportView } from '@/components/CaseReportView';
import { ArchitectureDiagram } from '@/components/ArchitectureDiagram';
import { Logo } from '@/components/Logo';
import { PhoneCallMockup } from '@/components/PhoneCallMockup';
import { createInvestigation, startInvestigation, getInvestigation } from '@/lib/api';
import { Investigation } from '@/types/investigation';

const DEMO_PRESETS = [
  {
    title: "ABC Bakery - Gluten-Free Policy",
    prompt: "Call ABC Bakery at (555) 019-2834 and ask if they make gluten-free wedding cakes and what advance notice is required."
  },
  {
    title: "Grand Harbor Hotel - Pet Policy",
    prompt: "Call Grand Harbor Hotel at (555) 019-7711 and ask if dogs are allowed in oceanview suites and what the pet deposit is."
  },
  {
    title: "Metro Auto Care - Brake Inspection",
    prompt: "Call Metro Auto Care at (555) 019-4488 and ask if they offer same-day brake inspection and estimated price."
  }
];

export default function Home() {
  const [mission, setMission] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentInvestigation, setCurrentInvestigation] = useState<Investigation | null>(null);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [startingCall, setStartingCall] = useState(false);

  const inputRef = useRef<HTMLTextAreaElement>(null);
  const archRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!currentInvestigation) return;
    const isLive = ['dialing', 'ivr', 'holding', 'speaking', 'analyzing'].includes(currentInvestigation.status);
    if (!isLive) return;

    const interval = setInterval(async () => {
      try {
        const updated = await getInvestigation(currentInvestigation.id);
        setCurrentInvestigation(updated);
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [currentInvestigation]);

  const handlePlanMission = async (textToSubmit?: string) => {
    const promptText = textToSubmit || mission;
    if (!promptText.trim()) return;

    setLoading(true);
    try {
      const inv = await createInvestigation(promptText);
      setCurrentInvestigation(inv);
      setShowConfirmation(true);
    } catch (err) {
      alert("Failed to plan mission: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmStart = async (phoneNumber: string, targetName: string) => {
    if (!currentInvestigation) return;
    setStartingCall(true);
    try {
      const updated = await startInvestigation(currentInvestigation.id, {
        phone_number: phoneNumber,
        target_name: targetName
      });
      setCurrentInvestigation(updated);
      setShowConfirmation(false);
    } catch (err) {
      alert("Failed to launch call: " + (err as Error).message);
    } finally {
      setStartingCall(false);
    }
  };

  const scrollToInput = () => {
    inputRef.current?.scrollIntoView({ behavior: 'smooth' });
    inputRef.current?.focus();
  };

  const scrollToArch = () => {
    archRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const isLive = currentInvestigation && ['dialing', 'ivr', 'holding', 'speaking', 'analyzing'].includes(currentInvestigation.status);

  return (
    <div className="w-full">
      {isLive ? (
        <div className="max-w-4xl mx-auto px-6 py-12">
          <LiveCallView investigation={currentInvestigation} />
        </div>
      ) : currentInvestigation && currentInvestigation.status === 'completed' ? (
        <div className="max-w-5xl mx-auto px-6 py-12">
          <CaseReportView
            investigation={currentInvestigation}
            onNewMission={() => {
              setCurrentInvestigation(null);
              setMission('');
            }}
          />
        </div>
      ) : (
        <div>
          {/* Hero Section with Adjacent Phone Call Mockup */}
          <section className="max-w-6xl mx-auto px-6 pt-16 pb-24 border-b border-gray-200">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              
              {/* Left Column: Text & Large Logo */}
              <div className="lg:col-span-7 space-y-8">
                <div className="flex items-center gap-4">
                  <Logo size={68} className="shadow-md" />
                  <div>
                    <span className="text-xs font-mono font-bold uppercase tracking-widest text-black block">
                      A Cross-Functional Architecture
                    </span>
                    <span className="text-xs font-mono text-gray-500 tracking-wider uppercase block mt-0.5">
                      Autonomous Telephony Intelligence &bull; 2026
                    </span>
                  </div>
                </div>

                <h1 className="text-5xl sm:text-6xl xl:text-7xl font-black tracking-tight text-black uppercase leading-[0.95]">
                  A Cross-Functional<br />
                  Architecture For<br />
                  Agentic Calls.
                </h1>

                <p className="text-lg text-gray-700 max-w-xl leading-relaxed font-sans">
                  An architecture for turning natural-language objectives into real phone conversations, evidence, and structured intelligence.
                </p>

                <div className="flex flex-wrap items-center gap-4 pt-2">
                  <button
                    onClick={scrollToInput}
                    className="px-8 py-4 bg-black text-white text-xs font-mono uppercase tracking-widest hover:bg-gray-800 transition-colors shadow-sm rounded-full"
                  >
                    Start An Investigation
                  </button>
                  <button
                    onClick={scrollToArch}
                    className="px-8 py-4 border border-black text-black text-xs font-mono uppercase tracking-widest hover:bg-black hover:text-white transition-colors rounded-full"
                  >
                    Explore The Architecture
                  </button>
                </div>
              </div>

              {/* Right Column: Adjacent Incoming Call Phone Mockup */}
              <div className="lg:col-span-5 flex justify-center lg:justify-end">
                <PhoneCallMockup />
              </div>

            </div>
          </section>

          {/* Interactive Mission Input Section */}
          <section className="max-w-4xl mx-auto px-6 py-20 border-b border-gray-200">
            <div className="space-y-8">
              <div className="border-b border-gray-200 pb-3 flex items-center justify-between">
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-black">
                  Dispatch Mission Terminal
                </span>
                <span className="text-xs font-mono text-gray-500">
                  Target Resolution &bull; CALL-E Voice
                </span>
              </div>

              {/* Demo Presets */}
              <div className="space-y-2">
                <span className="text-[11px] font-mono uppercase tracking-wider text-gray-500 block">
                  Quick Benchmark Presets:
                </span>
                <div className="flex flex-wrap gap-2">
                  {DEMO_PRESETS.map((preset, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setMission(preset.prompt);
                        handlePlanMission(preset.prompt);
                      }}
                      className="px-4 py-2 border border-gray-300 hover:border-black text-xs font-mono text-gray-800 hover:text-black bg-[#FAFAF9] transition-colors rounded-full"
                    >
                      &bull; {preset.title}
                    </button>
                  ))}
                </div>
              </div>

              {/* Text Input Terminal */}
              <div className="border border-black p-6 sm:p-8 bg-white shadow-sm space-y-6 rounded-3xl">
                <div>
                  <label className="block text-xs font-mono font-bold uppercase tracking-widest text-black mb-2">
                    Natural-Language Mission Prompt
                  </label>
                  <textarea
                    ref={inputRef}
                    rows={4}
                    value={mission}
                    onChange={(e) => setMission(e.target.value)}
                    placeholder="e.g. Call ABC Bakery at (555) 019-2834 and ask if they make gluten-free wedding cakes and what lead time is required."
                    className="w-full border border-gray-300 p-4 text-base text-black placeholder-gray-400 focus:outline-none focus:border-black font-sans leading-relaxed resize-y rounded-2xl"
                  />
                </div>

                <button
                  type="button"
                  disabled={loading || !mission.trim()}
                  onClick={() => handlePlanMission()}
                  className="w-full py-4 bg-black text-white text-xs font-mono uppercase tracking-widest hover:bg-gray-800 transition-colors disabled:opacity-40 flex items-center justify-center gap-3 font-semibold rounded-full"
                >
                  {loading ? (
                    <>
                      <span className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                      Decomposing Mission with Gemini AI...
                    </>
                  ) : (
                    'Plan Mission & Review Call Target'
                  )}
                </button>
              </div>
            </div>
          </section>

          {/* Section 01: The Problem */}
          <section className="max-w-6xl mx-auto px-6 py-24 border-b border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
              <div className="md:col-span-4">
                <span className="text-4xl sm:text-6xl font-mono font-black text-black block mb-2">
                  01
                </span>
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-gray-500 block">
                  The Problem
                </span>
              </div>
              <div className="md:col-span-8 space-y-4">
                <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-black">
                  Important information still lives inside phone conversations.
                </h2>
                <p className="text-base sm:text-lg text-gray-700 leading-relaxed font-sans">
                  The most valuable real-time operational data—custom pricing, lead times, unlisted inventory, emergency slot availability, and nuanced organizational policies—is never indexed on the public web. It requires a live telephony connection.
                </p>
              </div>
            </div>
          </section>

          {/* Section 02: The Architecture */}
          <section ref={archRef} className="max-w-6xl mx-auto px-6 py-24 border-b border-gray-200">
            <div className="space-y-10">
              <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
                <div className="md:col-span-4">
                  <span className="text-4xl sm:text-6xl font-mono font-black text-black block mb-2">
                    02
                  </span>
                  <span className="text-xs font-mono font-bold uppercase tracking-widest text-gray-500 block">
                    The Architecture
                  </span>
                </div>
                <div className="md:col-span-8">
                  <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-black">
                    A multi-stage orchestration pipeline from intent to verified report.
                  </h2>
                </div>
              </div>

              <ArchitectureDiagram />
            </div>
          </section>

          {/* Section 03: From Intent to Evidence */}
          <section className="max-w-6xl mx-auto px-6 py-24 border-b border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
              <div className="md:col-span-4">
                <span className="text-4xl sm:text-6xl font-mono font-black text-black block mb-2">
                  03
                </span>
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-gray-500 block">
                  Intent to Evidence
                </span>
              </div>
              <div className="md:col-span-8 space-y-6">
                <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-black">
                  Voice reasoning over real telephony infrastructure.
                </h2>
                <p className="text-base text-gray-700 leading-relaxed font-sans">
                  Unlike simulated text agents, telephony calls present noisy audio, complex touch-tone IVR routing trees, multi-minute hold queues, and sudden human interruptions. Our architecture continuously synchronizes DTMF signals, acoustics, and low-latency voice streaming.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 text-xs font-mono">
                  <div className="border border-gray-200 p-5 bg-[#FAFAF9] rounded-2xl">
                    <span className="font-bold text-black block mb-1">IVR TREE TRAVERSAL</span>
                    DTMF tone generation based on live acoustic menu options.
                  </div>
                  <div className="border border-gray-200 p-5 bg-[#FAFAF9] rounded-2xl">
                    <span className="font-bold text-black block mb-1">HOLD CLASSIFIER</span>
                    Acoustic music detection preventing timeout and premature hang-up.
                  </div>
                  <div className="border border-gray-200 p-5 bg-[#FAFAF9] rounded-2xl">
                    <span className="font-bold text-black block mb-1">EVIDENCE CAPTURE</span>
                    Immutable multi-speaker transcript logging with timestamps.
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 04: The Result */}
          <section className="max-w-6xl mx-auto px-6 py-24 border-b border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
              <div className="md:col-span-4">
                <span className="text-4xl sm:text-6xl font-mono font-black text-black block mb-2">
                  04
                </span>
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-gray-500 block">
                  The Result
                </span>
              </div>
              <div className="md:col-span-8 space-y-6">
                <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-black">
                  High-confidence verified intelligence dossiers.
                </h2>
                <p className="text-base text-gray-700 leading-relaxed font-sans">
                  Instead of ambiguous chatbot summaries, the final output is an executive-ready intelligence dossier. Every fact is mapped directly to audio transcript timestamps, and unsupported statements are strictly classified as &ldquo;Could not verify&rdquo;.
                </p>
                <div className="border border-gray-300 p-6 bg-[#FAFAF9] text-xs font-mono space-y-3 rounded-3xl">
                  <div className="flex justify-between border-b border-gray-200 pb-2">
                    <span className="font-bold text-black uppercase">Sample Output Dossier</span>
                    <span className="text-gray-500">Case #8F29A10C</span>
                  </div>
                  <div className="space-y-1 text-gray-700">
                    <p><span className="font-bold text-black">TARGET:</span> ABC Bakery &bull; (555) 019-2834</p>
                    <p><span className="font-bold text-black">EXECUTIVE SUMMARY:</span> Business confirmed availability of gluten-free certified wedding cakes with 72h notice.</p>
                    <p><span className="font-bold text-black">AUDIT TRAIL:</span> 100% audio verified across 182s call duration.</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Section 05: About Project */}
          <section className="max-w-6xl mx-auto px-6 py-24">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
              <div className="md:col-span-4">
                <span className="text-4xl sm:text-6xl font-mono font-black text-black block mb-2">
                  05
                </span>
                <span className="text-xs font-mono font-bold uppercase tracking-widest text-gray-500 block">
                  About Project
                </span>
              </div>
              <div className="md:col-span-8 space-y-6">
                <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-black">
                  Built for the hackathon stage. Designed for mission-critical operations.
                </h2>
                <p className="text-base text-gray-700 leading-relaxed font-sans">
                  A Cross-Functional Architecture for Agentic Calls bridges the gap between frontier LLM reasoning and real-world telephony infrastructure, creating a dependable foundation for autonomous business communication.
                </p>
                <div>
                  <Link
                    href="/about"
                    className="inline-block px-6 py-3 border border-black text-xs font-mono uppercase tracking-widest text-black hover:bg-black hover:text-white transition-colors rounded-full"
                  >
                    Read Full About Dossier &rarr;
                  </Link>
                </div>
              </div>
            </div>
          </section>
        </div>
      )}

      {showConfirmation && currentInvestigation && (
        <ConfirmationModal
          investigation={currentInvestigation}
          onConfirm={handleConfirmStart}
          onCancel={() => setShowConfirmation(false)}
          loading={startingCall}
        />
      )}
    </div>
  );
}
