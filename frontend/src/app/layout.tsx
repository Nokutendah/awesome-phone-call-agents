import type { Metadata } from 'next';
import './globals.css';
import { Header } from '@/components/Header';

export const metadata: Metadata = {
  title: 'A Cross-Functional Architecture for Agentic Calls',
  description: 'An orchestration architecture for turning natural-language objectives into real phone conversations, evidence, and structured intelligence.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-white text-black min-h-screen flex flex-col antialiased selection:bg-black selection:text-white">
        <Header />
        <main className="flex-1 w-full">
          {children}
        </main>
        <footer className="border-t border-gray-200 py-8 bg-[#F7F7F5] mt-20">
          <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-gray-500">
            <div>
              A Cross-Functional Architecture for Agentic Calls &bull; Telephony Intelligence
            </div>
            <div>
              Built for High-Precision Communications &amp; Information Verification
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
