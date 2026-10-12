export function rankJobs(jobs) {
  return [...jobs].sort((a, b) => b.priority - a.priority);
}
