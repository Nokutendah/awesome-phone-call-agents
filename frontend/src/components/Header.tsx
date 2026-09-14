import React from 'react';
import Link from 'next/link';

export function Header() {
  return (
    <header className="border-b border-gray-200 bg-white sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Animated marquee containing only text */}
        <div className="marquee overflow-hidden whitespace-nowrap">
          <div className="marquee-content flex items-center space-x-4">
            <span className="font-mono font-bold text-xs sm:text-sm uppercase tracking-widest text-black">
              THE FUTURE OF CALLING
            </span>
          </div>
        </div>

        <nav className="flex items-center gap-2 sm:gap-6 text-xs font-mono uppercase tracking-wider">
          <Link
            href="/"
            className="text-gray-700 hover:text-black font-semibold transition-colors px-3.5 py-1.5 rounded-full hover:bg-gray-100"
          >
            New Mission
          </Link>
          <Link
            href="/history"
            className="text-gray-700 hover:text-black font-semibold transition-colors px-3.5 py-1.5 rounded-full hover:bg-gray-100"
          >
            History
          </Link>
          <Link
            href="/architecture"
            className="text-gray-700 hover:text-black font-semibold transition-colors px-3.5 py-1.5 rounded-full hover:bg-gray-100"
          >
            Architecture
          </Link>
          <Link
            href="/about"
            className="text-gray-700 hover:text-black font-semibold transition-colors px-3.5 py-1.5 rounded-full hover:bg-gray-100"
          >
            About
          </Link>
        </nav>
      </div>
    </header>
  );
}
