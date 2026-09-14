import React from 'react';

interface LogoProps {
  className?: string;
  size?: number;
}

export function Logo({ className = "w-8 h-8", size = 32 }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 500 500"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`rounded-full flex-shrink-0 ${className}`}
    >
      {/* Outer Circle Ring */}
      <circle
        cx="250"
        cy="250"
        r="238"
        stroke="#5CB5FF"
        strokeWidth="24"
        fill="white"
      />
      {/* Inner Accent Ring */}
      <circle
        cx="250"
        cy="250"
        r="214"
        stroke="#5CB5FF"
        strokeWidth="8"
        strokeOpacity="0.8"
        fill="none"
      />

      {/* Smartphone Body */}
      <rect
        x="180"
        y="130"
        width="140"
        height="240"
        rx="28"
        stroke="#5CB5FF"
        strokeWidth="14"
        fill="white"
      />

      {/* Top Phone Speaker / Camera */}
      <line
        x1="230"
        y1="145"
        x2="270"
        y2="145"
        stroke="#5CB5FF"
        strokeWidth="8"
        strokeLinecap="round"
      />
      <circle
        cx="220"
        cy="145"
        r="3"
        fill="#5CB5FF"
      />

      {/* Phone Screen Top/Bottom Dividers */}
      <line
        x1="180"
        y1="160"
        x2="320"
        y2="160"
        stroke="#5CB5FF"
        strokeWidth="8"
      />
      <line
        x1="180"
        y1="340"
        x2="320"
        y2="340"
        stroke="#5CB5FF"
        strokeWidth="8"
      />

      {/* Bottom Home Button Pill */}
      <rect
        x="236"
        y="350"
        width="28"
        height="10"
        rx="5"
        fill="#5CB5FF"
      />

      {/* Center Phone Handset Icon */}
      <path
        d="M272 206 C280 214, 298 232, 298 244 C298 252, 288 266, 276 278 C264 290, 246 298, 238 298 C226 298, 208 280, 204 272 L228 254 L244 264 C250 258, 258 250, 264 244 L254 228 Z"
        stroke="#5CB5FF"
        strokeWidth="14"
        strokeLinejoin="round"
        strokeLinecap="round"
        fill="white"
      />
    </svg>
  );
}
