import React from 'react';

export function PhoneCallMockup() {
  return (
    <div className="relative mx-auto w-[280px] sm:w-[320px] bg-[#111111] border-4 border-[#222222] rounded-[44px] p-3 shadow-2xl ring-1 ring-black/10 transform rotate-1 hover:rotate-0 transition-transform duration-300">
      {/* Phone Screen Outer */}
      <div className="relative bg-[#09090b] rounded-[36px] overflow-hidden p-6 text-white flex flex-col justify-between h-[520px] select-none border border-white/5">
        
        {/* Dynamic Island / Notch */}
        <div className="absolute top-3 left-1/2 -translate-x-1/2 w-24 h-4 bg-black rounded-full flex items-center justify-end px-2">
          <div className="w-2 h-2 rounded-full bg-blue-500/80 animate-pulse"></div>
        </div>

        {/* Top Status & Incoming Call Header */}
        <div className="pt-8 text-center space-y-1">
          <p className="text-xs font-mono text-gray-400 tracking-wider uppercase">
            CALL-E Voice Network
          </p>
          <h4 className="text-2xl font-semibold tracking-tight text-gray-100">
            Incoming Call
          </h4>
        </div>

        {/* Center Caller Avatar & Info */}
        <div className="flex flex-col items-center justify-center space-y-4 my-auto">
          <div className="w-24 h-24 rounded-full bg-[#27272a] border border-white/10 flex items-center justify-center shadow-inner">
            <svg
              className="w-12 h-12 text-[#d4d4d8]"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
            </svg>
          </div>

          <div className="text-center">
            <h5 className="text-xl font-bold text-white tracking-wide">
              Target Entity
            </h5>
            <p className="text-xs font-mono text-blue-400 mt-0.5">
              Live Investigation Line
            </p>
          </div>
        </div>

        {/* Bottom Options & Call Controls */}
        <div className="space-y-6 pb-4">
          {/* Quick Option Icons */}
          <div className="flex justify-around text-[10px] font-mono text-gray-400 px-4">
            <div className="flex flex-col items-center gap-1">
              <div className="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center text-white text-xs">
                &#9200;
              </div>
              <span>Remind Me</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <div className="w-9 h-9 rounded-full bg-white/10 flex items-center justify-center text-white text-xs">
                &#128172;
              </div>
              <span>Message</span>
            </div>
          </div>

          {/* Decline & Accept Buttons */}
          <div className="flex items-center justify-around px-2 pt-1">
            {/* Decline Button (Red) */}
            <div className="flex flex-col items-center gap-1.5">
              <div className="w-16 h-16 rounded-full bg-[#ef4444] hover:bg-[#dc2626] flex items-center justify-center text-white shadow-lg transition-transform hover:scale-105 cursor-pointer">
                <svg className="w-7 h-7 rotate-[135deg]" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" />
                </svg>
              </div>
              <span className="text-[10px] font-mono text-gray-400">Decline</span>
            </div>

            {/* Accept Button (Green) */}
            <div className="flex flex-col items-center gap-1.5">
              <div className="w-16 h-16 rounded-full bg-[#22c55e] hover:bg-[#16a34a] flex items-center justify-center text-white shadow-lg transition-transform hover:scale-105 animate-pulse cursor-pointer">
                <svg className="w-7 h-7" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" />
                </svg>
              </div>
              <span className="text-[10px] font-mono text-gray-400">Accept</span>
            </div>
          </div>
        </div>

        {/* Bottom Home Indicator Bar */}
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 w-32 h-1 bg-white/40 rounded-full"></div>
      </div>
    </div>
  );
}
