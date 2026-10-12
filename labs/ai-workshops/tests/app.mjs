export function retryDelay(value, now) {
  return Number.parseInt(value, 10) * 1000;
}
