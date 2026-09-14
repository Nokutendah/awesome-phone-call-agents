import React from 'react';
import Link from 'next/link';
import { Investigation } from '@/types/investigation';

interface InvestigationHistoryProps {
  investigations: Investigation[];
}

export function InvestigationHistory({ investigations }: InvestigationHistoryProps) {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between border-b-2 border-black pb-6 gap-4">
        <div>
          <span className="text-xs font-mono uppercase tracking-widest text-gray-500 block mb-1">
            Archive // Telephony Records
          </span>
          <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-black uppercase">
            Investigation History
          </h1>
        </div>
        <Link
          href="/"
          className="px-6 py-2.5 bg-black text-white text-xs font-mono uppercase tracking-wider hover:bg-gray-800 transition-colors inline-block rounded-full"
        >
          + Launch New Mission
        </Link>
      </div>

      {investigations.length === 0 ? (
        <div className="p-16 text-center border border-gray-200 bg-[#FAFAF9] text-gray-500 space-y-2 rounded-3xl">
          <p className="text-sm font-mono uppercase tracking-wide text-black font-semibold">
            No Previous Telephony Investigations Found
          </p>
          <p className="text-xs text-gray-500">
            Submit a natural-language mission to start capturing phone intelligence.
          </p>
        </div>
      ) : (
        <div className="border border-gray-200 divide-y divide-gray-200 bg-white rounded-3xl overflow-hidden shadow-sm">
          {investigations.map((item) => {
            const isDone = item.status === 'completed';
            const verifiedCount = item.answers
              ? item.answers.filter(a => a.verification === 'verified').length
              : 0;

            return (
              <div
                key={item.id}
                className="p-6 hover:bg-[#FAFAF9] transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-6"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-3 text-xs font-mono">
                    <span className="border border-black px-3 py-0.5 font-bold uppercase text-black rounded-full">
                      {item.status.toUpperCase()}
                    </span>
                    <span className="text-gray-500">
                      {new Date(item.created_at || item.timestamp).toLocaleString()}
                    </span>
                    <span className="text-gray-400">
                      ID: {item.id.slice(0, 8)}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold text-black tracking-tight pt-1">
                    {item.target_name || 'Target Line'}
                  </h3>

                  <p className="text-xs text-gray-600 font-mono">
                    Target: {item.phone_number || 'N/A'} &bull; Prompt: &ldquo;{item.mission.slice(0, 90)}...&rdquo;
                  </p>
                </div>

                <div className="flex items-center gap-6 sm:border-l sm:border-gray-200 sm:pl-6">
                  {isDone && (
                    <div className="text-right font-mono text-xs hidden md:block">
                      <div className="font-bold text-black">{verifiedCount} Answers Verified</div>
                      <div className="text-gray-500">{item.duration_seconds}s Call Duration</div>
                    </div>
                  )}

                  <Link
                    href={`/investigation/${item.id}`}
                    className="px-5 py-2 border border-gray-300 hover:border-black text-xs font-mono uppercase tracking-wider text-black transition-colors whitespace-nowrap rounded-full"
                  >
                    View Dossier &rarr;
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
