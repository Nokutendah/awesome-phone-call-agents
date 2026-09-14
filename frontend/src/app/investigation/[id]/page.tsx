'use client';

import React, { useEffect, useState } from 'react';
import { LiveCallView } from '@/components/LiveCallView';
import { CaseReportView } from '@/components/CaseReportView';
import { getInvestigation } from '@/lib/api';
import { Investigation } from '@/types/investigation';
import Link from 'next/link';

export default function InvestigationDetailPage({ params }: { params: { id: string } }) {
  const resolvedParams = params;
  const [investigation, setInvestigation] = useState<Investigation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getInvestigation(resolvedParams.id);
        setInvestigation(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [resolvedParams.id]);

  useEffect(() => {
    if (!investigation) return;
    const isLive = ['dialing', 'ivr', 'holding', 'speaking', 'analyzing'].includes(investigation.status);
    if (!isLive) return;

    const interval = setInterval(async () => {
      try {
        const updated = await getInvestigation(investigation.id);
        setInvestigation(updated);
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [investigation]);

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      {loading ? (
        <div className="py-20 text-center text-gray-500 font-mono text-xs flex flex-col items-center gap-3">
          <span className="h-5 w-5 border-2 border-gray-300 border-t-black rounded-full animate-spin"></span>
          Retrieving investigation dossier from local database...
        </div>
      ) : error || !investigation ? (
        <div className="p-12 text-center border border-gray-300 bg-[#FAFAF9] space-y-4 max-w-lg mx-auto">
          <p className="text-black font-mono text-sm font-bold">{error || 'Investigation record not found'}</p>
          <Link
            href="/history"
            className="inline-block px-4 py-2 border border-black text-xs font-mono uppercase tracking-wider text-black hover:bg-black hover:text-white transition-colors"
          >
            &larr; Return to Investigation History
          </Link>
        </div>
      ) : ['dialing', 'ivr', 'holding', 'speaking', 'analyzing'].includes(investigation.status) ? (
        <div className="max-w-4xl mx-auto">
          <LiveCallView investigation={investigation} />
        </div>
      ) : (
        <CaseReportView investigation={investigation} />
      )}
    </div>
  );
}
