'use client';

import React from 'react';
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="max-w-2xl mx-auto px-6 py-24 text-center space-y-6">
      <span className="text-xs font-mono uppercase tracking-widest text-gray-500 block">
        404 // Resource Not Found
      </span>
      <h1 className="text-4xl font-black uppercase text-black">
        Endpoint Undefined
      </h1>
      <p className="text-sm text-gray-600 font-mono">
        The requested telephony record or dossier endpoint does not exist.
      </p>
      <div className="pt-4">
        <Link
          href="/"
          className="inline-block px-6 py-3 bg-black text-white text-xs font-mono uppercase tracking-wider hover:bg-gray-800 transition-colors"
        >
          Return to Terminal &rarr;
        </Link>
      </div>
    </div>
  );
}
