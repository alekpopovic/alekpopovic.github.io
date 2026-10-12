export function retryDelay(value, now) {
  if (typeof value !== 'string' || !Number.isFinite(now)) return null;
  const text = value.trim();
  if (/^\d+$/.test(text)) {
    const seconds = Number(text);
    return Number.isSafeInteger(seconds * 1000) ? seconds * 1000 : null;
  }
  if (!/^[A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} GMT$/.test(text)) return null;
  const date = Date.parse(text);
  return Number.isFinite(date) && new Date(date).toUTCString() === text ? Math.max(0, date - now) : null;
}
