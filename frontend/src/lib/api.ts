import { Investigation } from '@/types/investigation';

const API_BASE = '/api';

export async function createInvestigation(mission: string): Promise<Investigation> {
  const res = await fetch(`${API_BASE}/investigations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mission }),
  });
  if (!res.ok) {
    throw new Error(`Failed to create investigation: ${res.statusText}`);
  }
  return res.json();
}

export async function startInvestigation(id: string, overrides?: { phone_number?: string; target_name?: string }): Promise<Investigation> {
  const res = await fetch(`${API_BASE}/investigations/${id}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(overrides || {}),
  });
  if (!res.ok) {
    throw new Error(`Failed to start investigation: ${res.statusText}`);
  }
  return res.json();
}

export async function getInvestigation(id: string): Promise<Investigation> {
  const res = await fetch(`${API_BASE}/investigations/${id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch investigation: ${res.statusText}`);
  }
  return res.json();
}

export async function listInvestigations(): Promise<Investigation[]> {
  const res = await fetch(`${API_BASE}/investigations`);
  if (!res.ok) {
    throw new Error(`Failed to list investigations: ${res.statusText}`);
  }
  return res.json();
}
