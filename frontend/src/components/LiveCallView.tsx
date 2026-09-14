import React from 'react';
import { Investigation, InvestigationStatus } from '@/types/investigation';

interface LiveCallViewProps {
  investigation: Investigation;
}

const statusBadgeConfig: Record<InvestigationStatus, { label: string; color: string }> = {
  draft: { label: 'Drafting', color: 'text-gray-600 border-gray-300' },
  ready: { label: 'Ready to Dial', color: 'text-gray-600 border-gray-300' },
  dialing: { label: 'Dialing', color: 'text-gray-600 border-gray-300' },
  ivr: { label: 'Navigating IVR', color: 'text-gray-600 border-gray-300' },
  holding: { label: 'On Hold', color: 'text-gray-600 border-gray-300' },
  speaking: { label: 'Speaking', color: 'text-gray-600 border-gray-300' },
  analyzing: { label: 'Analyzing', color: 'text-gray-600 border-gray-300' },
  completed: { label: 'Completed', color: 'text-gray-600 border-gray-300' },
  failed: { label: 'Failed', color: 'text-red-600 border-red-600' },
  needs_user_input: { label: 'Action Required', color: 'text-orange-600 border-orange-600' },
};

export function LiveCallView({ investigation }: LiveCallViewProps) {
  const cfg = statusBadgeConfig[investigation.status] || statusBadgeConfig.dialing;
  const isLive = ['dialing', 'ivr', 'holding', 'speaking', 'analyzing'].includes(investigation.status);

  return (
    <div className="space-y-6">
      <div className="p-6 sm:p-8 rounded-3xl bg-white border border-gray-200 space-y-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-200 pb-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className={`inline-flex items-center px-3 py-1 border text-xs font-semibold rounded-full ${cfg.color}`}>
                {cfg.label}
              </span>
              <span className="text-xs text-gray-500 font-mono">ID: {investigation.id.slice(0, 8)}</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
              {investigation.target_name || 'Target Business'}
            </h2>
            <p className="text-sm font-mono text-gray-400 mt-1">
              Phone: {investigation.phone_number || 'Unspecified'}
            </p>
          </div>

          <div className="flex items-center gap-6 text-sm text-gray-600 bg-gray-50 px-4 py-2 rounded-full border border-gray-200">
            <div>Duration: <strong>{investigation.duration_seconds}s</strong></div>
            <div className="w-px h-4 bg-gray-300"></div>
            <div>Hold: <strong>{investigation.hold_seconds}s</strong></div>
          </div>
        </div>

        {isLive && (
          <div className="flex items-center gap-2 px-3 py-1 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-mono rounded-full w-fit">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
            Audio channel active
          </div>
        )}

        {/* Live Audio Transcript Stream */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-gray-800 uppercase tracking-wider flex items-center gap-2">
            <span>Live Audio Transcript</span>
            {isLive && <span className="text-xs text-gray-500 font-mono font-normal animate-pulse">(Streaming live...)</span>}
          </h3>

          <div className="max-h-96 overflow-y-auto border border-gray-200 rounded-2xl p-4 text-sm text-gray-800 bg-[#FAFAF9]">
            {investigation.transcript && investigation.transcript.length > 0 ? (
              investigation.transcript.map((item, idx) => (
                <div key={idx} className="mb-3 p-3 bg-white border border-gray-200 rounded-xl shadow-xs">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span className="font-bold text-black uppercase">{item.speaker}</span>
                    <span>{item.timestamp}</span>
                  </div>
                  <p className="text-gray-800">{item.text}</p>
                </div>
              ))
            ) : (
              <p className="text-gray-500 italic py-4 text-center">Awaiting transcript stream from CALL-E...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
