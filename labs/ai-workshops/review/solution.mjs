export function requestEvent(request) {
  return { event: 'request_finished', method: request.method,
    path: request.url.split(/[?#]/, 1)[0], status: request.status, duration_ms: request.duration_ms };
}
