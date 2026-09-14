'use client';

import React, { useState, useEffect } from 'react';
import { InvestigationHistory } from '@/components/InvestigationHistory';
import { listInvestigations } from '@/lib/api';
import { Investigation } from '@/types/investigation';

export default function HistoryPage() {
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await listInvestigations();
        setInvestigations(data);
      } catch (err) {
        console.error("Failed to load history:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      {loading ? (
        <div className="py-20 text-center text-gray-500 font-mono text-xs flex flex-col items-center gap-3">
          <span className="h-5 w-5 border-2 border-gray-300 border-t-black rounded-full animate-spin"></span>
          Querying local SQLite investigation records...
        </div>
      ) : (
        <InvestigationHistory investigations={investigations} />
      )}
    </div>
  );
}
