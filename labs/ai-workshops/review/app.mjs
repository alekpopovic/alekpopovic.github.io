export function requestEvent(request) {
  return { ...request, event: 'request_finished' };
}
