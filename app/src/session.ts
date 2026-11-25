// Morning / afternoon class handling.
//
// The Day 14 lab runs 14:00 to 18:00 (afternoon class); the deck writes slide times in
// afternoon clock time. The morning class runs the same 240 minutes, shifted by
// MORNING_SHIFT_HOURS. Change that one number if the morning class starts at another time.
//
// Slide content is written in afternoon times. localize() shifts every HH:MM between 13:00 and
// 18:59 for the morning class, and fills the {{SESSION}} / {{SESSION_RANGE}} / {{DEADLINE}} tokens.

export type Session = 'morning' | 'afternoon'

/** Hour (local time) from which the deck opens as the afternoon class. */
export const AFTERNOON_FROM_HOUR = 13

/** Morning class = afternoon schedule moved this many hours earlier (14:00 to 09:00). */
export const MORNING_SHIFT_HOURS = -5

const AFTERNOON_START = '14:00'
const AFTERNOON_END = '18:00'

export const SESSION_LABEL: Record<Session, string> = {
  morning: 'Lớp sáng',
  afternoon: 'Lớp chiều',
}

/** Submission deadline (GMT+7) per class. Day 14: both classes submit by 23h59 on the lab day. */
export const DEADLINE: Record<Session, string> = {
  morning: '23h59 ngày lab',
  afternoon: '23h59 ngày lab',
}

const PARAM = 'ca'
const PARAM_VALUE: Record<Session, string> = { morning: 'sang', afternoon: 'chieu' }

/** Session forced by the URL (?ca=sang or ?ca=chieu), if any. */
export function sessionFromUrl(): Session | null {
  const v = new URLSearchParams(window.location.search).get(PARAM)
  if (v === PARAM_VALUE.morning) return 'morning'
  if (v === PARAM_VALUE.afternoon) return 'afternoon'
  return null
}

/** Session from the clock at the moment the deck opens. */
export function sessionFromClock(now: Date = new Date()): Session {
  return now.getHours() < AFTERNOON_FROM_HOUR ? 'morning' : 'afternoon'
}

/** Write the chosen session into the URL so a reload or a shared link keeps it. */
export function pinSessionInUrl(session: Session) {
  const url = new URL(window.location.href)
  url.searchParams.set(PARAM, PARAM_VALUE[session])
  window.history.replaceState(null, '', url)
}

export function clearSessionInUrl() {
  const url = new URL(window.location.href)
  url.searchParams.delete(PARAM)
  window.history.replaceState(null, '', url)
}

function shiftTime(hhmm: string, hours: number) {
  const [h, m] = hhmm.split(':').map(Number)
  return `${String(h + hours).padStart(2, '0')}:${String(m).padStart(2, '0')}`
}

const TIME_RE = /\b(1[3-8]):([0-5]\d)\b/g

/** Localize slide HTML or a title for a session. */
export function localize(text: string, session: Session): string {
  const shift = session === 'morning' ? MORNING_SHIFT_HOURS : 0
  const range = `${shiftTime(AFTERNOON_START, shift)} đến ${shiftTime(AFTERNOON_END, shift)}`
  // Shift the slide times first, then fill the tokens. The range is already shifted, so it must
  // not pass through TIME_RE again (18:00 -> 13:00 would become 08:00).
  let out = text
  if (shift !== 0) {
    out = out.replace(TIME_RE, (_, h: string, m: string) => shiftTime(`${h}:${m}`, shift))
  }
  return out
    .replaceAll('{{SESSION}}', SESSION_LABEL[session])
    .replaceAll('{{SESSION_RANGE}}', range)
    .replaceAll('{{DEADLINE}}', DEADLINE[session])
}
