// Client-side helper: send a lead to the Highland Travel group form system.
// The backend records the source site from the request Origin, needs at least
// one contact method (phone / wechat / email) and answers { success: true }.

export const LEAD_ENDPOINT = 'https://form.highland-travel.com';
export const FALLBACK_EMAIL = 'support@approvedtilers.co.uk';

export interface Lead {
  name?: string;
  phone?: string;
  wechat?: string;
  email?: string;
  address?: string;
  start_date?: string;
  end_date?: string;
  tour: string;
  contact_method?: string;
  message?: string;
}

/** "Label: value" lines for the free-text message, skipping empty values. */
export function buildMessage(pairs: Array<[string, string | null | undefined]>): string {
  return pairs
    .filter(([, v]) => v && v.trim())
    .map(([k, v]) => `${k}: ${v!.trim()}`)
    .join('\n');
}

/** Resolves true only when the endpoint responds with a 2xx status. */
export async function submitLead(lead: Lead): Promise<boolean> {
  const body = Object.fromEntries(
    Object.entries(lead).filter(([, v]) => typeof v === 'string' && v.trim() !== '')
  );
  try {
    const response = await fetch(LEAD_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return response.ok;
  } catch {
    return false;
  }
}
