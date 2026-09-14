export type InvestigationStatus =
  | 'draft'
  | 'ready'
  | 'dialing'
  | 'ivr'
  | 'holding'
  | 'speaking'
  | 'analyzing'
  | 'completed'
  | 'failed'
  | 'needs_user_input';

export type ConfidenceLevel = 'high' | 'medium' | 'low';
export type VerificationState = 'verified' | 'unverified' | 'not_answered' | 'contradicted';

export interface QuestionAnswer {
  question: string;
  answer: string;
  confidence: ConfidenceLevel;
  verification: VerificationState;
}

export interface TranscriptEntry {
  speaker: string;
  text: string;
  timestamp: string;
}

export interface Investigation {
  id: string;
  mission: string;
  status: InvestigationStatus;
  target_name?: string | null;
  phone_number?: string | null;
  planned_questions: string[];
  summary?: string | null;
  answers: QuestionAnswer[];
  representative?: string | null;
  duration_seconds: number;
  hold_seconds: number;
  timestamp: string;
  transcript: TranscriptEntry[];
  recording_url?: string | null;
  created_at: string;
  updated_at: string;
}
