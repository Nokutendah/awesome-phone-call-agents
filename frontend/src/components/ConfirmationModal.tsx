import React, { useState } from 'react';
import { Investigation } from '@/types/investigation';

interface ConfirmationModalProps {
  investigation: Investigation;
  onConfirm: (phoneNumber: string, targetName: string) => void;
  onCancel: () => void;
  loading: boolean;
}

export function ConfirmationModal({ investigation, onConfirm, onCancel, loading }: ConfirmationModalProps) {
  const [phoneNumber, setPhoneNumber] = useState(investigation.phone_number || '');
  const [targetName, setTargetName] = useState(investigation.target_name || '');
  const [error, setError] = useState('');

  const handleStart = () => {
    if (!phoneNumber.trim()) {
      setError('A valid phone number is required before launching the call.');
      return;
    }
    setError('');
    onConfirm(phoneNumber.trim(), targetName.trim() || 'Target Line');
  };

  const isMissingInfo = !investigation.phone_number || investigation.status === 'needs_user_input';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div className="bg-white border border-gray-300 p-6 sm:p-8 max-w-xl w-full shadow-2xl space-y-6 rounded-3xl">
        <div className="flex items-start justify-between border-b border-gray-200 pb-4">
          <div>
            <div className="inline-block border border-black px-3 py-0.5 text-[10px] font-mono font-bold uppercase tracking-wider mb-2 rounded-full">
              Step 03 &bull; Target Verification
            </div>
            <h3 className="text-xl font-bold text-black tracking-tight">Review Mission Call Target</h3>
          </div>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-black font-mono text-xl leading-none w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
          >
            &times;
          </button>
        </div>

        {isMissingInfo && (
          <div className="p-4 border border-gray-300 bg-[#FAFAF9] text-xs text-gray-700 leading-relaxed font-mono rounded-2xl">
            <span className="font-bold text-black block mb-1">PHONE NUMBER REQUIRED</span>
            The target phone number could not be resolved from natural language input. Please verify or input the destination phone number below.
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-gray-600 mb-1.5">
              Target Organization / Business Name
            </label>
            <input
              type="text"
              value={targetName}
              onChange={(e) => setTargetName(e.target.value)}
              placeholder="e.g. ABC Bakery"
              className="w-full border border-gray-300 px-4 py-2.5 text-sm text-black placeholder-gray-400 focus:outline-none focus:border-black font-sans rounded-xl"
            />
          </div>

          <div>
            <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-gray-600 mb-1.5">
              Destination Phone Number
            </label>
            <input
              type="text"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="e.g. (555) 019-2834"
              className="w-full border border-gray-300 px-4 py-2.5 text-sm text-black placeholder-gray-400 focus:outline-none focus:border-black font-mono rounded-xl"
            />
            {error && <p className="text-red-600 text-xs font-mono mt-1">{error}</p>}
          </div>

          <div>
            <label className="block text-xs font-mono font-semibold uppercase tracking-wider text-gray-600 mb-2">
              Planned Verification Questions ({investigation.planned_questions.length})
            </label>
            <div className="space-y-2 max-h-48 overflow-y-auto border border-gray-200 p-3 bg-[#FAFAF9] rounded-2xl">
              {investigation.planned_questions.map((q, idx) => (
                <div key={idx} className="text-xs text-gray-800 flex items-start gap-2">
                  <span className="font-mono font-bold text-black">{idx + 1}.</span>
                  <span>{q}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            onClick={onCancel}
            className="px-5 py-2.5 border border-gray-300 text-xs font-mono uppercase tracking-wider text-gray-700 hover:border-black hover:text-black transition-colors rounded-full"
          >
            Cancel
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={handleStart}
            className="px-6 py-2.5 bg-black text-white text-xs font-mono uppercase tracking-wider hover:bg-gray-800 transition-colors disabled:opacity-50 flex items-center gap-2 rounded-full"
          >
            {loading ? (
              <>
                <span className="h-3 w-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Initiating Telephony...
              </>
            ) : (
              'Confirm & Launch Call'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
