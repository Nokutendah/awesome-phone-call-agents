import React from 'react';

interface Stage {
  num: string;
  name: string;
  sub: string;
  desc: string;
}

const STAGES: Stage[] = [
  {
    num: "01",
    name: "INTENT",
    sub: "Natural Language",
    desc: "Unstructured user requirement or investigation goal"
  },
  {
    num: "02",
    name: "PLANNING",
    sub: "Mission Decomposition",
    desc: "Gemini decomposes target questions & conversational boundaries"
  },
  {
    num: "03",
    name: "RESOLUTION",
    sub: "Target & Entity Resolution",
    desc: "Extracts phone endpoint, organization, & operational hours"
  },
  {
    num: "04",
    name: "EXECUTION",
    sub: "Agentic Voice Call",
    desc: "Autonomous CALL-E connection over SIP/PSTN trunk"
  },
  {
    num: "05",
    name: "NAVIGATION",
    sub: "IVR / Phone Systems",
    desc: "Real-time DTMF & intent navigation through audio trees"
  },
  {
    num: "06",
    name: "CONVERSATION",
    sub: "Human-to-Agent Dialog",
    desc: "Low-latency bidirectional speech with business representatives"
  },
  {
    num: "07",
    name: "EVIDENCE",
    sub: "Audio & Raw Transcript",
    desc: "Bit-level call recording, turn timestamps, and speaker labels"
  },
  {
    num: "08",
    name: "INTELLIGENCE",
    sub: "Extraction & Verification",
    desc: "Fact verification, contradiction checks, and uncertainty bounds"
  },
  {
    num: "09",
    name: "REPORT",
    sub: "Structured Dossier",
    desc: "Executive summary, verified claims, and permanent audit trail"
  }
];

export function ArchitectureDiagram() {
  return (
    <div className="w-full bg-white border border-gray-200 p-8 sm:p-12 rounded-3xl shadow-sm">
      <div className="mb-10 flex flex-col sm:flex-row sm:items-end justify-between border-b border-gray-200 pb-6 gap-4">
        <div>
          <span className="text-xs font-mono uppercase tracking-widest text-gray-500 block mb-1">
            System Topology // Spec v2.4
          </span>
          <h3 className="text-2xl sm:text-3xl font-bold tracking-tight text-black">
            Cross-Functional Telephony Architecture
          </h3>
        </div>
        <div className="text-xs font-mono text-gray-500 px-3 py-1 bg-gray-100 rounded-full">
          END-TO-END PIPELINE: INTENT &rarr; VERIFIED INTELLIGENCE
        </div>
      </div>

      {/* Engineering Process Steps Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {STAGES.map((stage, idx) => (
          <div
            key={stage.num}
            className="border border-gray-200 p-6 bg-[#FAFAF9] hover:bg-white hover:border-black transition-colors relative flex flex-col justify-between rounded-2xl"
          >
            <div>
              <div className="flex items-baseline justify-between border-b border-gray-200 pb-3 mb-4">
                <span className="text-3xl sm:text-4xl font-mono font-black text-black tracking-tight">
                  {stage.num}
                </span>
                <span className="text-[10px] font-mono uppercase tracking-widest text-gray-500 bg-white border border-gray-200 px-3 py-0.5 rounded-full">
                  Phase 0{idx + 1}
                </span>
              </div>
              <h4 className="text-lg font-bold text-black tracking-tight mb-0.5">
                {stage.name}
              </h4>
              <p className="text-xs font-mono font-semibold text-gray-600 mb-3 uppercase tracking-wide">
                {stage.sub}
              </p>
              <p className="text-xs text-gray-600 leading-relaxed">
                {stage.desc}
              </p>
            </div>
            
            {idx < STAGES.length - 1 && (
              <div className="mt-4 pt-3 border-t border-gray-200/60 flex items-center justify-between text-[11px] font-mono text-gray-400">
                <span>FORWARD PIPELINE</span>
                <span>&darr;</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Engineering Pipeline Flow Footer */}
      <div className="mt-8 pt-6 border-t border-gray-200 flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-gray-500">
        <div>
          <span className="font-bold text-black uppercase">Zero Hallucination Policy:</span> Unverified claims marked as &ldquo;Could not verify&rdquo;
        </div>
        <div className="px-3 py-1 bg-gray-100 rounded-full">
          LATENCY TARGET: &lt;450ms &bull; PROTOCOL: SIP/WebRTC &bull; VERIFICATION: Strict
        </div>
      </div>
    </div>
  );
}
