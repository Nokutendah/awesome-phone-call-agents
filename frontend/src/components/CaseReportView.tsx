import React, { useState } from 'react';
import { Investigation, VerificationState } from '@/types/investigation';

interface CaseReportViewProps {
  investigation: Investigation;
  onNewMission?: () => void;
}

const verificationLabels: Record<VerificationState, string> = {
  verified: 'VERIFIED',
  unverified: 'COULD NOT VERIFY',
  not_answered: 'NOT ANSWERED',
  contradicted: 'CONTRADICTED',
};

export function CaseReportView({ investigation, onNewMission }: CaseReportViewProps) {
  const [showFullTranscript, setShowFullTranscript] = useState(true);

  const verifiedCount = investigation.answers
    ? investigation.answers.filter(a => a.verification === 'verified').length
    : 0;
  const totalQuestions = investigation.answers?.length || investigation.planned_questions?.length || 0;

  return (
    <div className="max-w-4xl mx-auto bg-white border border-gray-300 p-8 sm:p-14 shadow-sm space-y-12 rounded-3xl">
      {/* Top Header Actions */}
      <div className="flex flex-wrap items-center justify-between border-b-2 border-black pb-6 gap-4">
        <div>
          <span className="text-xs font-mono uppercase tracking-widest text-gray-500 block mb-1">
            Official Intelligence Dossier // Case #{investigation.id.slice(0, 8)}
          </span>
          <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-black uppercase">
            Investigation Report
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {onNewMission && (
            <button
              onClick={onNewMission}
              className="px-5 py-2 border border-black text-xs font-mono uppercase tracking-wider text-black hover:bg-black hover:text-white transition-colors rounded-full"
            >
              + New Mission
            </button>
          )}
          <button
            onClick={() => window.print()}
            className="px-4 py-2 bg-gray-100 border border-gray-300 text-xs font-mono uppercase tracking-wider text-gray-700 hover:bg-gray-200 transition-colors rounded-full"
          >
            Print Dossier
          </button>
        </div>
      </div>

      {/* Metadata Specification Table */}
      <div className="border border-gray-200 bg-[#FAFAF9] p-6 rounded-2xl">
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-6 text-xs font-mono">
          <div>
            <span className="text-gray-500 uppercase block mb-1">Target</span>
            <span className="font-bold text-black text-sm block">
              {investigation.target_name || 'Target Line'}
            </span>
          </div>
          <div>
            <span className="text-gray-500 uppercase block mb-1">Phone</span>
            <span className="font-bold text-black text-sm block">
              {investigation.phone_number || 'N/A'}
            </span>
          </div>
          <div>
            <span className="text-gray-500 uppercase block mb-1">Date</span>
            <span className="font-bold text-black text-sm block">
              {new Date(investigation.timestamp).toLocaleDateString()}
            </span>
          </div>
          <div>
            <span className="text-gray-500 uppercase block mb-1">Duration</span>
            <span className="font-bold text-black text-sm block">
              {investigation.duration_seconds}s ({investigation.hold_seconds}s hold)
            </span>
          </div>
          <div>
            <span className="text-gray-500 uppercase block mb-1">Status</span>
            <span className="inline-block px-3 py-0.5 border border-black text-black font-bold uppercase rounded-full">
              {investigation.status.toUpperCase()}
            </span>
          </div>
        </div>
      </div>

      {/* Executive Summary Section */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <h2 className="text-sm font-mono font-bold uppercase tracking-widest text-black">
            01 // Executive Summary
          </h2>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            {verifiedCount}/{totalQuestions} Claims Verified
          </span>
        </div>
        <p className="text-base text-gray-800 leading-relaxed font-sans font-normal">
          {investigation.summary || 'Summary pending call completion.'}
        </p>
      </section>

      {/* Questions & Findings Section */}
      <section className="space-y-6">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <h2 className="text-sm font-mono font-bold uppercase tracking-widest text-black">
            02 // Questions &amp; Findings
          </h2>
          <span className="text-xs font-mono text-gray-500 px-3 py-0.5 bg-gray-100 rounded-full">
            Strict Fact-Verification Policy
          </span>
        </div>

        <div className="divide-y divide-gray-200 border-t border-b border-gray-200">
          {investigation.answers && investigation.answers.length > 0 ? (
            investigation.answers.map((qa, idx) => {
              const isVerified = qa.verification === 'verified';
              return (
                <div key={idx} className="py-6 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-xs font-bold text-black bg-gray-100 border border-gray-300 px-2.5 py-0.5 rounded-full">
                        Q0{idx + 1}
                      </span>
                      <h3 className="font-bold text-base text-black">{qa.question}</h3>
                    </div>
                    <span
                      className={`text-xs font-mono px-3 py-0.5 border uppercase font-semibold rounded-full ${
                        isVerified
                          ? 'border-black text-black bg-gray-50'
                          : 'border-gray-300 text-gray-500 bg-gray-50'
                      }`}
                    >
                      {verificationLabels[qa.verification] || qa.verification.toUpperCase()}
                    </span>
                  </div>

                  <div className="pl-9">
                    <p className={`text-sm leading-relaxed ${isVerified ? 'text-gray-900' : 'text-gray-600 italic'}`}>
                      {qa.answer}
                    </p>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="py-6 text-sm text-gray-500 font-mono">
              No structured Q&amp;A points extracted.
            </div>
          )}
        </div>
      </section>

      {/* Audio Recording */}
      {investigation.recording_url && (
        <section className="space-y-4">
          <div className="flex items-center justify-between border-b border-gray-200 pb-2">
            <h2 className="text-sm font-mono font-bold uppercase tracking-widest text-black">
              03 // Telephony Audio Evidence
            </h2>
            <span className="text-xs font-mono text-gray-500">Bitstream Recording</span>
          </div>
          <div className="border border-gray-200 p-4 bg-[#FAFAF9] flex flex-wrap items-center justify-between gap-4 rounded-2xl">
            <div className="text-xs font-mono text-gray-600">
              <span className="font-bold text-black block">Raw Call Audio ({investigation.duration_seconds}s)</span>
              <span>URL: {investigation.recording_url}</span>
            </div>
            <audio controls src={investigation.recording_url} className="h-8 rounded-full" />
          </div>
        </section>
      )}

      {/* Evidence / Transcript Section */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-2">
          <h2 className="text-sm font-mono font-bold uppercase tracking-widest text-black">
            {investigation.recording_url ? '04' : '03'} // Evidence &amp; Call Transcript
          </h2>
          <button
            onClick={() => setShowFullTranscript(!showFullTranscript)}
            className="text-xs font-mono text-gray-600 hover:text-black underline uppercase"
          >
            {showFullTranscript ? 'Collapse' : 'Expand'} ({investigation.transcript?.length || 0} Turns)
          </button>
        </div>

        {showFullTranscript && (
          <div className="border border-gray-200 divide-y divide-gray-100 text-xs font-mono bg-white max-h-[500px] overflow-y-auto rounded-2xl">
            {investigation.transcript && investigation.transcript.length > 0 ? (
              investigation.transcript.map((item, idx) => (
                <div key={idx} className="p-4 hover:bg-[#FAFAF9] transition-colors">
                  <div className="flex items-center justify-between text-gray-500 mb-1">
                    <span className="font-bold text-black uppercase">{item.speaker}</span>
                    <span>{item.timestamp}</span>
                  </div>
                  <p className="text-gray-800 font-sans text-sm leading-relaxed">{item.text}</p>
                </div>
              ))
            ) : (
              <div className="p-4 text-gray-500 italic">No transcript turns captured.</div>
            )}
          </div>
        )}
      </section>

      {/* Footer / Verification Stamp */}
      <div className="pt-8 border-t border-gray-200 flex flex-wrap items-center justify-between text-xs font-mono text-gray-500 gap-4">
        <div>
          AUTONOMOUS VERIFICATION SYSTEM &bull; REPORT GENERATED {new Date().toISOString()}
        </div>
        <div className="border border-gray-400 px-4 py-1.5 text-black font-bold uppercase tracking-wider rounded-full">
          VERIFIED DOSSIER
        </div>
      </div>
    </div>
  );
}
